from db import db

class ItemModel(db.Model):
    __tablename__ = 'items'
    
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))
    
    store_id = db.Column(db.Integer,db.ForeignKey('stores.id')) # store_id in items table will be a foreign key to id column in stores table.
    store = db.relationship('StoreModel') # We dont have joins in sqlalchemy, by defining this way it will go 
    #and check if we have a given store_id,In the StoreModel.
    
    def __init__(self,name,price,store_id):
        self.name = name
        self.price = price
        self.store_id = store_id
        
    def json(self):
        return {'name': self.name,'price': self.price}
    
    @classmethod
    def find_by_name(cls,name):
        return cls.query.filter_by(name=name).first() # This statement is equal to SELECT * FROM items WHERE name=name
    # Here .query is provided SQLAlchemy which denotes that we are building a query and filter_by is another word for WHERE condition.
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
        
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()