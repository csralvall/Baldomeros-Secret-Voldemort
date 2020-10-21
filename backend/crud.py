<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
from pony.orm import db_session, select, count
from .database import *

@db_session #Bool
def user_is_registred(name, upassword):
    try:
        u = User.get(Username = name, Password = upassword)
        if u:
            return True
        else: 
            return False
    except Exception:
        return False

@db_session
def check_username(username):
    try: 
        u = User.exists(Username=username)
        return u 
    except Exception:
        return False

@db_session
def check_email(email):
    try: 
        u = User.exists(Email=email)
        return u 
    except Exception:
        return False

@db_session #get the User object.
def get_user(username, password):
    user = User.get(Username=username, Password=password)
    if user is not None:
        user = user.to_dict("Id Username")
    return user

=======
from .database import *
>>>>>>> SV-51 #time 10m #comment setting database, nothing to test. #done
=======
=======
>>>>>>> SV-34 #comment Metodos agregados.
from pony.orm import *
from .database import *

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
<<<<<<< HEAD
>>>>>>> Feature/sv 21 registro bd (#4)
=======

=======
from pony.orm import db_session, select, count
from .database import *
>>>>>>> c0554b3... SV-34 #time 10m #comment changed check_mail and check_username. added get_user

@db_session #Bool
def user_is_registred(name, upassword):
    try:
        u = User.get(Username = name, Password = upassword)
        if u:
            return True
        else: 
            return False
    except Exception:
        return False

@db_session
def check_username(username):
    try: 
        u = User.exists(Username=username)
        return u 
    except Exception:
        return False

@db_session
def check_email(email):
    try: 
        u = User.exists(Email=email)
        return u 
    except Exception:
        return False
<<<<<<< HEAD
=======

@db_session #get the User object.
def get_user(username, password):
    user = User.get(Username=username, Password=password)
    if user is not None:
        user = user.to_dict("Id Username")
    return user

>>>>>>> c0554b3... SV-34 #time 10m #comment changed check_mail and check_username. added get_user
>>>>>>> SV-34 #comment Metodos agregados.
