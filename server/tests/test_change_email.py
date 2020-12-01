from fastapi.testclient import TestClient

from server.db.crud.exception_crud import *
from server.db.crud.crud_deck import *
from server.db.crud.crud_election import *
from server.db.crud.crud_legislative_session import *
from server.db.crud.crud_lobby import *
from server.db.crud.crud_match import *
from server.db.crud.crud_messages import *
from server.db.crud.crud_profile import *
from server.db.crud.crud_spell import *


from server.db.dicts import *

from server.main import app

from server.tests.helpers import *

client = TestClient(app)

def test_change_email_ok():
    delete_data(Board)
    delete_data(Player)
    delete_data(Match)
    delete_data(User)

    create_user("one@gmail.com","one","old")
    aux = get_user("one", "old")
    auxid = aux["Id"] 

    olde = get_email(auxid)
    newe = "newone@gmail.com"

    response = client.post(
        f"/email?user_id={auxid}&olde={olde}&newe={newe}"
    )

    assert response.status_code == 200

def test_change_email_bad_user():
    delete_data(Board)
    delete_data(Player)
    delete_data(Match)
    delete_data(User)

    create_user("one@gmail.com","one","old")
    aux = get_user("one", "old")
    auxid = aux["Id"]

    create_user("two@gmail.com","two","old2")
    aux2 = get_user("two", "old2")
    auxid2 = aux2["Id"] 

    olde = get_email(auxid)
    newe = "newone@gmail.com"

    response = client.post(
        f"/email?user_id={auxid2}&olde={olde}&newe={newe}"
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "invalid user or email"} 

def test_change_email_bad_email():
    delete_data(Board)
    delete_data(Player)
    delete_data(Match)
    delete_data(User)

    create_user("one@gmail.com","one","old")
    aux = get_user("one", "old")
    auxid = aux["Id"]

    create_user("two@gmail.com","two","old2")
    aux2 = get_user("two", "old2")
    auxid2 = aux2["Id"] 

    olde2 = get_email(auxid2)
    newe = "newone@gmail.com"

    response = client.post(
        f"/email?user_id={auxid}&olde={olde2}&newe={newe}"
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "invalid user or email"} 
