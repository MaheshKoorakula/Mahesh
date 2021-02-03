from models.user import UserModel

def authenticate(username,password):
    user = UserModel.find_by_username(username) # if the user is not found, set the default value as None.
    if user and user.password == password:
        return user
    
def identity(payload):
    user_id = payload['identity']
    return UserModel.find_by_id(user_id) # if the id is not found, set the default value as None.