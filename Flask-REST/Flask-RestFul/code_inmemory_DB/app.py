from flask import Flask, request
from flask_restful import Resource, Api, reqparse  # Api is imported from the Flask RestFul to easily take Resource into it. 
from flask_jwt import JWT, jwt_required
from security import authenticate, identity

app = Flask(__name__)
app.secret_key = 'Mahesh' # Whenever we create a secret key, it has to be long complex.
api = Api(app)

jwt = JWT(app,authenticate,identity) # To JWT we pass our function and both authenticate and identity functions from security file.
# JWT creates the /auth endpoint.

items = [
    
]

class Item(Resource):
    parser = reqparse.RequestParser()
        parser.add_argument('price',
                type=float,
                required=True,
                help="This field cannot be left blank!"
            )
        
    @jwt_required()
    def get(self,name):
        item = next(filter(lambda x: x['name'] == name, items), None)
        return {'item': item} , 200 if item else 404 # It gives status 200 if the item exists and 404 if the item does not exist.
    
    def post(self,name):
        if next(filter(lambda x: x['name'] == name, items), None):
            return {'message': "An item with name '{}' already exists.".format(name)} , 400
        
        data = Item.parser.parse_args()
        
        data = request.get_json(silent=True) # if we are not sure that what type of data our client might give us i.e., when content-type is not json
        # We can set force = True which will forcefully format the data into json type and does not throw an error.
        # If we dont want to process the client everytime even though the content-type is set correctly. We can use silent = True, which will not process the data.
        # But, also does not throw an error if the content-type is not set. 
        item = {'name': name, 'price': data['price']}
        items.append(item)
        return item , 201 # 201 is the HTTP status code for "Created".
    
    def delete(self,name):
        global items
        items = list(filter(lambda x: x['name'] != name, items))
        return {'message': 'Item deleted.'}
    
    def put(self,name):
        data = Item.parser.parse_args()
        item = next(filter(lambda x: x['name'] != name, items), None)
        if item is None:
            item = {'name': name, 'price': data['price']}
            items.append(item)
        else:
            item.update(data) # Dictionaries have a method called update which updates the entire item with the data received.
        return item
    
class ItemList(Resource):
    def get(self):
        return {'items': items}
    

api.add_resource(Item,'/item/<string:name>') #http:127.0.0.1:5000/item/Rolf
api.add_resource(ItemList, '/items')

app.run(debug=True)