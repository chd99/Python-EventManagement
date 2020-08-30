import sqlite3
from flask import Flask, request
from flask_restful import Resource


class Event(Resource):

    def find_event(self, event_id):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM events WHERE event_id=?"
        result = cursor.execute(query, (event_id,))
        row = result.fetchone()

        connection.close()
        if row:
            return {'event': {'event_id': row[0], 'name': row[1], 'location': row[2], 'startDate': row[3], 'endDate': row[4]}}

    def insert(self, event):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "INSERT INTO events VALUES (?,?,?,?,?)"
        cursor.execute(query, (event['event_id'], event['name'], event['location'], event['startDate'], event['endDate']))

        connection.commit()
        connection.close()

    def update(self, event):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "UPDATE events SET name=?, location=?, startDate=?, endDate=? WHERE event_id=?"
        cursor.execute(query, (event['name'], event['location'], event['startDate'], event['endDate'], event['event_id']))

        connection.commit()
        connection.close()

    ## view event
    def get(self, event_id):
        event = self.find_event(event_id)
        if event:
            return event
        return {'message': 'Event is not found.'}, 404

    ## create event
    def post(self, event_id):
        if self.find_event(event_id):
            return {'message': "An event with event_id '{}' already exists.".format(event_id)}, 400

        data = request.get_json()
        event = {'event_id': event_id,
                 'name': data['name'],
                 'location': data['location'],
                 'startDate': data['startDate'],
                 'endDate': data['endDate']
                 }

        try:
            self.insert(event)
        except:
            return {"message": "An error occurred inserting the event."}, 500

        return event, 201

    def delete(self, event_id):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "DELETE FROM events WHERE event_id=?"
        result = cursor.execute(query, (event_id,))

        connection.commit()
        connection.close()
        return {'message': 'event deleted.'}

    ## create or update if exist
    def put(self, event_id):
        data = request.get_json()

        event = self.find_event(event_id)
        updated_event = {'event_id': event_id,
                         'name': data['name'],
                         'location': data['location'],
                         'startDate': data['startDate'],
                         'endDate': data['endDate']
                         }
        if event is None:
            try:
                self.insert(updated_event)
            except:
                return {"message": "An error occurred inserting the event."}, 500
        else:
            try:
                self.update(updated_event)
            except:
                return {"message": "An error occurred updating the event."}, 500
        return updated_event


class EventList(Resource):
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM events"
        result = cursor.execute(query)
        events = []
        for row in result:
            events.append({'event_id': row[0], 'name': row[1], 'location': row[2], 'startDate': row[3], 'endDate': row[4]})

        connection.close()
        return {'events': events}
