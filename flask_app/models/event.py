from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user

DB = 'pencild_n'
class Event: 
    def __init__(self, data):
        self.id = data['id']
        self.event_name = data['event_name']
        self.event_date = data['event_date']
        self.event_start = data['event_start']
        self.event_end = data['event_end']

    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM events LEFT JOIN users on events.user_id = users.id WHERE events.id = %(id)s;"
        result = connectToMySQL(DB).query_db(query,data)
        result = result[0] #only want the top result, hence the result[0]
        event = cls(result)
        data = {
                'id' : result['users.id'],
                'first_name': result['first_name'],
                'last_name': result['last_name'],
                'email' : result['email'],
                'password' : result['password'],
                'created_at' : result['users.created_at'],
                'updated_at': result['users.updated_at']
        }
        event.coordinator = user.User(data)
        return event
    
    @classmethod
    def get_all_for_user(cls, user_id):
        query = """
        SELECT events.*, users.id as 'users.id', users.first_name, users.last_name, users.email, users.password, users.created_at as 'users.created_at', users.updated_at as 'users.updated_at' FROM events
        LEFT JOIN users on events.user_id = users.id
        WHERE events.user_id = %(user_id)s
        UNION
        SELECT events.*, users.id as 'users.id', users.first_name, users.last_name, users.email, users.password, users.created_at as 'users.created_at', users.updated_at as 'users.updated_at' FROM events
        JOIN user_events ON events.id = user_events.event_id
        LEFT JOIN users ON events.user_id = users.id
        WHERE user_events.user_id = %(user_id)s;
    """
        data = {'user_id': user_id}
        results = connectToMySQL(DB).query_db(query, data)
    
        events = [] 
        if results:
            for row in results:
                this_event = cls(row)
                user_data = {
                    'id': row['users.id'],
                    'first_name': row['first_name'],
                    'last_name': row['last_name'],
                    'email': row['email'],
                    'password': "",
                    'created_at': row['users.created_at'],
                    'updated_at': row['users.updated_at'], 
                    'profile_picture': ""
                }
                this_event.coordinator = user.User(user_data)
                events.append(this_event)
        return events
    
    @classmethod
    def get_all(cls):
        query = "SELECT *, TIME_FORMAT(event_start, '%h:%i %p') FROM events LEFT JOIN users on events.user_id = users.id;"
        results = connectToMySQL(DB).query_db(query)
        print(results)
        events = [] 
        for row in results:
            this_event = cls(row)
            user_data = {
                'id': row['users.id'],
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'email': row['email'],
                'password': "",
                'created_at': row['users.created_at'],
                'updated_at': row['users.updated_at'],
                'profile_picture': ""
            }
            this_event.coordinator = user.User(user_data)
            events.append(this_event)
        return events
    
    @classmethod
    def save(cls, data):
        query = "INSERT INTO events (event_name, event_date, event_start, event_end, user_id) VALUES (%(event_name)s, %(event_date)s, %(event_start)s, %(event_end)s, %(user_id)s);"
        return connectToMySQL(DB).query_db(query, data)
    
    @classmethod
    def save_for_user(cls, user_id, event_id):
        query = "INSERT INTO user_events (user_id, event_id) VALUES (%(user_id)s, %(event_id)s);"
        data = {
            'user_id': user_id,
            'event_id': event_id,
        }
        return connectToMySQL(DB).query_db(query, data)
    
    @classmethod
    def update(cls, data):
        query = "UPDATE events SET event_name = %(event_name)s, event_start = %(event_start)s, event_end = %(event_end)s WHERE id = %(id)s;"
        return connectToMySQL(DB).query_db(query, data)
    
    @classmethod
    def delete(cls, data):
        query = "DELETE FROM events WHERE id = %(id)s;"
        return connectToMySQL(DB).query_db(query, data)