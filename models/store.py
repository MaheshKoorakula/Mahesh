from db import db

class StoreModel(db.Model):
    __tablename__ = 'stores'
    
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(80))
    
    items = db.relationship('ItemModel',lazy='dynamic') # This is called reverse referencing, by defining this way sqlalchemy thinks that it has a relationship with ItemModel.
    # So it goes and checks in the ItemModel and finds out that it has a foreign key reference coming from ItemModel for store id. 
    # If we don't set lazy = dynamic, for every item created it goes and checks the store_id and creates a relationship if matchec. This is will cost the performance.
    # To avoid that, we have to dynamic lazy=dynamic.
    def __init__(self,name):
        self.name = name
        
    def json(self):
        return {'name': self.name, 'items': [item.json() for item in self.items.all()]} # Here we call .all() function to fetch all the items which match the store_id.
    # Now, this is when we check if there is an item in our ItemModel matching the store id and create the relationship if exists.
    
    @classmethod
    def find_by_name(cls,name):
        return cls.query.filter_by(name=name).first()
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
        
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()