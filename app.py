from flask import Flask
from flask_restful import Api 
from flask_jwt import JWT
from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item,ItemList
from resources.store import Store,StoreList

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # Since we have both Flask-SQLAlchemy and SQLAlchemy each of them has its own personl DB changes tracker.
# So we deactivate the underlying Flask-SQLAlchemy tracker, so that we can use SQLAlchemy tracker.
app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key = 'Mahesh' # Whenever we create a secret key, it has to be long complex.
api = Api(app)

jwt = JWT(app,authenticate,identity) # To JWT we pass our function and both authenticate and identity functions from security file.
# JWT creates the /auth endpoint.

api.add_resource(Store,'/store/<string:name>')
api.add_resource(StoreList,'/stores')
api.add_resource(Item,'/item/<string:name>') #http:127.0.0.1:5000/item/Rolf
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister,'/register')


if __name__ == '__main__': # We write this line to tell python that run the app, only when this file is considered as main.
    # i.e., In python, when we run the app.py file it will be considered as main file and if we import app.py in someother file
    # and run that file, that will be considered as main file.
    from db import db
    db.init_app(app)
    app.run(port=5000,debug=True)