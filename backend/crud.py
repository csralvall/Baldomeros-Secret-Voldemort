from pony.orm import db_session, select, count
from . import database
#Falta importar archivos de /backend.
#Una vez decidido los nombres agregar.

@db_session
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
def check_username(name):
    try:
        u = User.get(Username = name)
        if u:
            return True
        else: 
            return False
    except Exception:
        return False

@db_session
def check_mail(mail):
    try:
        u = User.get(Email = mail)
        if u:
            return True
        else: 
            return False
    except Exception:
        return False