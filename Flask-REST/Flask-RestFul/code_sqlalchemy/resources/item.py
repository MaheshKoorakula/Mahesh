from flask_restful import Resource,reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                type=float,
                required=True,
                help="This field cannot be left blank!"
            )
    parser.add_argument('store_id',
                type=float,
                required=True,
                help="Every item needs a store id."
            )
        
    @jwt_required()
    def get(self,name):
        item = ItemModel.find_by_name(name) # Since find_by_name returns the class object.
        if item:
            return item.json() # We have to convert the object to json, using .json() function.
        else:
            return {'message': 'Item not found'}, 404
    
    def post(self,name):
        if ItemModel.find_by_name(name): # Generally find_by_name is class method we call them using classname.functionname
            return {'message': "An item with name '{}' already exists.".format(name)} , 400 # 400 status code = Request error.
        
        data = Item.parser.parse_args()
        
        #data = request.get_json(silent=True) # if we are not sure that what type of data our client might give us i.e., when content-type is not json
        # We can set force = True which will forcefully format the data into json type and does not throw an error.
        # If we dont want to process the client everytime even though the content-type is set correctly. We can use silent = True, which will not process the data.
        # But, also does not throw an error if the content-type is not set. 
        item = ItemModel(name,data['price'],data['store_id'])
        
        try:
            item.save_to_db()
        except:
            return {"message": "An error occurred inserting the item."},500 # 500 status code = Internal server error.
        return item.json() , 201 # 201 is the HTTP status code for "Created".
    
    def delete(self,name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return {'message': 'Item deleted.'}
        return {'message': 'Item not found.'}
    
    def put(self,name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)
        
        if item is None:
            item = ItemModel(name,data['price'],data['store_id'])
        else:
            item.price = data['price'] # Because item is uniquely identified by its id.
        
        item.save_to_db()
        
        return item.json()
  
  
class ItemList(Resource):
    def get(self):        
        return {'items': list(map(lambda x: x.json(), ItemModel.query.all()))} # .all() gives all the rows from the items table.