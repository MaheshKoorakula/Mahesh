import sqlite3

connection = sqlite3.connect('data.db') #sqlite3 works by storing all of its data in a file, we define that as data.db

cursor = connection.cursor() # Cursor is responsible for executing queries and store the result.

create_table = "CREATE TABLE users (id int, username text, password text)"

cursor.execute(create_table)

user = (1,'Mahesh','asdf')
insert_query = "INSERT INTO users values (?,?,?)"
cursor.execute(insert_query,user)

users = [
    (2,'rolf','asdf'),
    (3,'anne','xyz')
]

cursor.executemany(insert_query,users)

select_query = "SELECT * FROM users"
for row in cursor.execute(select_query):
    print(row)

connection.commit()
connection.close()

