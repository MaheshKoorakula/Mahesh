import sqlite3
from db import db

class UserModel(db.Model):
    __tablename__ = 'users' # __tablename__ variable is used tell the SQLAlchemy about the table we are going to use.
    
    id = db.Column(db.Integer,primary_key=True) # We define the column names in the SQLAlchemny in this way.
    # It tells that column name is id which is of type Integer and is also a primary key.
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))
    
    def __init__(self,username,password):
        #self.id = _id # Here we use _id because id is a python keyword.
        self.username = username # The class variables self.id,self.username,self.password has to match with the column names to store in the DB.
        self.password = password # if we create anyother class variables that wont store in the DB and also wont give an error.
        
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
        
    @classmethod    
    def find_by_username(cls,username): # Since we dont use the self anywhere, we can change it to class method.
        return cls.query.filter_by(username=username).first() # first() is used to return the first row of the returned value.
    
    @classmethod    
    def find_by_id(cls,_id): # Since we dont use the self anywhere, we can change it to class method.
        return cls.query.filter_by(id=_id).first()