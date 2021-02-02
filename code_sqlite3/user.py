import sqlite3
from flask_restful import Resource, reqparse

class User:
    def __init__(self,_id,username,password):
        self.id = _id # Here we use _id because id is a python keyword.
        self.username = username
        self.password = password
        
    @classmethod    
    def find_by_username(cls,username): # Since we dont use the self anywhere, we can change it to class method.
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        
        query = "SELECT * FROM users WHERE username=?"
        result = cursor.execute(query,(username,)) # We have to pass the values as tuples to the query always like (username,) with comma in the end.
        # Because if we define as (username), the value in the brackets takes the precedence and gets executed first. Since it is just a value and not a query,
        # It does not return any value.
        row = result.fetchone() # fetchone() returns the first row of the result.
        if row:
            user = cls(*row) # instead of passing row[0],row[1],row[2] we can pass *row and vice versa.
        else:
            user = None
        
        connection.close()
        return user
    
    @classmethod    
    def find_by_id(cls,_id): # Since we dont use the self anywhere, we can change it to class method.
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        
        query = "SELECT * FROM users WHERE id=?"
        result = cursor.execute(query,(_id,)) # We have to pass the values as tuples to the query always like (username,) with comma in the end.
        # Because if we define as (username), the value in the brackets takes the precedence and gets executed first. Since it is just a value and not a query,
        # It does not return any value.
        row = result.fetchone() # fetchone() returns the first row of the result.
        if row:
            user = cls(*row) # instead of passing row[0],row[1],row[2] we can pass *row and vice versa.
        else:
            user = None
        
        connection.close()
        return user

class UserRegister(Resource):
    
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="This field cannot be blank.")
    
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="This field cannot be blank.")
    
    def post(self):
        data = UserRegister.parser.parse_args()
        
        if User.find_by_username(data['username']):
            return {"message": "A user with that username already exists."}, 400
        
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        
        query = "INSERT INTO users VALUES (NULL,?,?)"
        cursor.execute(query,(data['username'],data['password'],))

        connection.commit()
        connection.close()
        
        return {"message": "User created Successfully."} , 201 # 201 is the status for Created.