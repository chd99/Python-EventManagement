import sqlite3
from flask import Flask, request
from flask_restful import Resource
from flask_mail import Mail, Message

app = Flask(__name__)
mail = Mail(app)  # instantiate the mail class

# configuration of mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'chinteki@gmail.com'
app.config['MAIL_PASSWORD'] = 'Cd913562@'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

MAIL_DEFAULT_RECIPIENT = "chinteki@gmail.com"

class RegisteredUser(Resource):
    def get(self, user_mail):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT r.register_id, r.user_mail, r.registered_eventid, e.name, e.location, e.startDate, e.endDate  " \
                "FROM register as r, events as e " \
                "WHERE r.user_mail=? AND r.registered_eventid = e.event_id"
        result = cursor.execute(query, (user_mail,))
        registeredEvents = []
        for row in result:
            registeredEvents.append({'register_id': row[0],
                                     'user_mail': row[1],
                                     'event_id': row[2],
                                     'event_name': row[3],
                                     'event_location': row[4],
                                     'startDate': row[5],
                                     'endDate': row[6]
                                     })

        connection.close()
        if registeredEvents:
            return {'RegisteredEvents': registeredEvents}
        return {'message': 'The user has no registered event.'}, 404


class Register(Resource):
    def find_event(self, event_id):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM events WHERE event_id=?"
        result = cursor.execute(query, (event_id,))
        row = result.fetchone()

        connection.close()
        if row:
            return {'event': {'event_id': row[0], 'name': row[1], 'location': row[2], 'startDate': row[3], 'endDate': row[4]}}

    def check_register(self, register):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM register WHERE user_mail=? AND registered_eventid=?"
        result = cursor.execute(query, (register['user_mail'], register['event_id'],))
        row = result.fetchone()

        connection.close()
        if row:
            return {'registered': {'register_id': row[0], 'user_mail': row[1], 'registered_eventid': row[2]}}


    def insert(self, register):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "INSERT INTO register(user_mail, registered_eventid) VALUES (?,?)"
        cursor.execute(query, (register['user_mail'], register['event_id']))

        connection.commit()
        connection.close()

    def post(self, event_id):
        if not self.find_event(event_id):
            return {'message': "The event with event_id '{}' does not exist.".format(event_id)}, 400

        data = request.get_json()
        register = {'user_mail': data['user_mail'],
                    'event_id': data['event_id']
                    }

        if self.check_register(register):
            return {'message': "This user({}) has registered the event with event_id({}).".format(register['user_mail'], register['event_id'])}, 200

        try:
            self.insert(register)
        except:
            return {"message": "An error occurred registering the event."}, 500

## todo: Haven't make the send notice mail function working.  comment out
#        self.send_mail(register)
        return register, 201


    def send_mail(self, register):
        msg = Message(
            'Notice',
            sender=app.config.get("MAIL_USERNAME"),
            recipients=MAIL_DEFAULT_RECIPIENT
        )
        msg.body = 'Notice: User {} registered event (event_id:{}).' .format(register['user_mail'], register['event_id'])
        mail.send(msg)
        return 'Sent'

class DeleteRegister(Resource):
    def find_delete(self, deleteRegister):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM register WHERE user_mail=? AND registered_eventid=?"
        result = cursor.execute(query, (deleteRegister['user_mail'], deleteRegister['event_id'],))
        row = result.fetchone()

        connection.close()
        if row:
            return {'registered': {'register_id': row[0], 'user_mail': row[1], 'registered_eventid': row[2]}}

    def delete(self):
        data = request.get_json()
        deleteRegister = {'user_mail': data['user_mail'],
                          'event_id': data['event_id']
                          }
        if not self.find_delete(deleteRegister):
            return {'message': "This register does not exist."}, 400

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "DELETE FROM register WHERE user_mail=? AND registered_eventid=?"
        cursor.execute(query, (deleteRegister['user_mail'], deleteRegister['event_id'],))

        connection.commit()
        connection.close()
        return {'message': 'register deleted.'}
