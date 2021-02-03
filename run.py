from app import app
from db import db

db.ini(app)

@app.before_first_request
def create_tables(): # This will execute before the first request can be made and will create all the tables which are required in the script.
    # Also, by storing the values in the data.db file.
    db.create_all()