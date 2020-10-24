from pony.orm import *
from .model import *

@db_session
def create_user(email: str, username: str, password: str):
    try:
        User(Email=email, Username=username, Password=password)
        return True
    except Exception:
        return False


#needed for testing
@db_session
def delete_data(table):
    delete(p for p in table)