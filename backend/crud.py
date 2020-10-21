from pony.orm import db_session, select, count
#Falta importar archivos de /backend.
#Una vez decidido los nombres agregar.

@db_session
def consulta_user(name, upassword):
    try:
        u = User.get(Username = name, Password = upassword)
        if u:
            return True
        else: 
            return False
    except Exception:
        return False