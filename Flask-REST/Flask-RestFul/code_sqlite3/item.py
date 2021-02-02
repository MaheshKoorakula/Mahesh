import sqlite3
from flask_restful import Resource,reqparse
from flask_jwt import jwt_required

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                type=float,
                required=True,
                help="This field cannot be left blank!"
            )
        
    @jwt_required()
    def get(self,name):
        item = self.find_by_name(name)
        if item:
            return item
        else:
            return {'message': 'Item not found'}, 404
    
    @classmethod
    def find_by_name(cls,name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        
        query = "SELECT * FROM items WHERE name=?"
        result = cursor.execute(query,(name,))
        row = result.fetchone()
        connection.close()
        
        if row:
            return {'item': {'name': row[0], 'price': row[1]}}
    
    def post(self,name):
        if self.find_by_name(name): # Generally find_by_name is class method we call them using classname.functionname
            return {'message': "An item with name '{}' already exists.".format(name)} , 400 # 400 status code = Request error.
        
        data = Item.parser.parse_args()
        
        #data = request.get_json(silent=True) # if we are not sure that what type of data our client might give us i.e., when content-type is not json
        # We can set force = True which will forcefully format the data into json type and does not throw an error.
        # If we dont want to process the client everytime even though the content-type is set correctly. We can use silent = True, which will not process the data.
        # But, also does not throw an error if the content-type is not set. 
        item = {'name': name, 'price': data['price']}
        
        try:
            self.insert(item)
        except:
            return {"message": "An error occurred inserting the item."},500 # 500 status code = Internal server error.
        return item , 201 # 201 is the HTTP status code for "Created".
    
    @classmethod
    def insert(cls,item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        
        query = "INSERT INTO items VALUES(?,?)"
        cursor.execute(query,(item['name'],item['price']))
        
        connection.commit()
        connection.close()
    
    def delete(self,name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        
        query = "DELETE FROM items WHERE name=?"
        cursor.execute(query,(name,))
        
        connection.commit()
        connection.close()
        
        return {'message': 'Item deleted.'}
    
    def put(self,name):
        data = Item.parser.parse_args()
        item = self.find_by_name(name)
        updated_item = {'name': name, 'price': data['price']}
        if item is None:
            try:
                self.insert(updated_item)
            except:
                return {"message": "An error occured inserting the item."}, 500
        else:
            try:
                self.update(updated_item)
            except:
                return {"message": "An error occured updating the item."}, 500
        return updated_item
    
    @classmethod
    def update(cls,item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        
        query = "UPDATE items SET price=? WHERE name=?"
        cursor.execute(query,(item['price'],item['name']))
        
        connection.commit()
        connection.close()
    
class ItemList(Resource):
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        
        query = "SELECT * FROM items"
        result = cursor.execute(query)
        items = []
        for row in result:
            items.append({'name': row[0],'price': row[1]})
        
        connection.close()
        
        return {'items': items}