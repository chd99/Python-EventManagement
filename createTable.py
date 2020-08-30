import sqlite3

connection = sqlite3.connect('data.db')
cursor = connection.cursor()

## events master table
create_table = "CREATE TABLE IF NOT EXISTS events (" \
               "event_id text PRIMARY KEY NOT NULL, " \
               "name text, " \
               "location text, " \
               "startDate Date, " \
               "endDate Date " \
               ")"
cursor.execute(create_table)

## register info table
create_table = "CREATE TABLE IF NOT EXISTS register (" \
               "register_id INTEGER PRIMARY KEY AUTOINCREMENT," \
               "user_mail text NOT NULL, " \
               "registered_eventid text " \
               ")"
cursor.execute(create_table)

## sample data insert
event = ('ev0001', 'test_Matrix', 'test_Beijing', '2020-08-01', '2020-08-02')
insert_query = "INSERT INTO events VALUES (?,?,?,?,?)"
cursor.execute(insert_query, event)

register = ('sample@gmail.com', 'ev0001')
insert_query = "INSERT INTO register (user_mail, registered_eventid) VALUES (?,?)"
cursor.execute(insert_query, register)

select_query = "SELECT * FROM events"
for row in cursor.execute(select_query):
    print(row)

select_query = "SELECT * FROM register"
for row in cursor.execute(select_query):
    print(row)

connection.commit()

connection.close()
