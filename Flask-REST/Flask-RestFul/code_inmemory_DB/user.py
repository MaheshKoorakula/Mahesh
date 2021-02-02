class User:
    def __init__(self,_id,username,password):
        self.id = _id # Here we use _id because id is a python keyword.
        self.username = username
        self.password = password