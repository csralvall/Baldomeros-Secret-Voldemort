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

def test_change_password_ok():
    delete_data(Board)
    delete_data(Player)
    delete_data(Match)
    delete_data(User)

    create_user("one@gmail.com","one","old")
    aux = get_user("one", "old")
    auxid = aux["Id"] 

    oldp = get_password(auxid)
    newp = "new"

    response = client.post(
        f"/password?user_id={auxid}&oldp={oldp}&newp={newp}"
    )

    assert response.status_code == 200

def test_change_password_bad_user():
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

    oldp = get_password(auxid)
    newp = "new"

    response = client.post(
        f"/password?user_id={auxid2}&oldp={oldp}&newp={newp}"
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "invalid user or password"} 

def test_change_password_bad_password():
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

    oldp2 = get_password(auxid2)
    newp = "new"

    response = client.post(
        f"/password?user_id={auxid}&oldp={oldp2}&newp={newp}"
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "invalid user or password"} 