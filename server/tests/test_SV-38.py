from fastapi.testclient import TestClient

from server.db.crud import *

from server.tests.helpers import *

from server.main import app

client = TestClient(app)


def test_gamestatus_ok():
    delete_data(Board)
    delete_data(Player)
    delete_data(Match)
    delete_data(User)

    create_user("rt@gmail.com", "rteee", "rteee")
    aux = get_user("rteee", "rteee")
    auxid = aux["Id"] 

    gidaux = add_match_db("5", "5", auxid)
    gidauxid = gidaux["Match_id"]

    response = client.get(
        f"/game/{gidauxid}"
    )

    assert response.status_code == 200

def test_gamestatus_fail_mid():
    delete_data(Board)
    delete_data(Player)
    delete_data(Match)
    delete_data(User)

    create_user("rt@gmail.com", "rteee", "rteee")
    aux = get_user("rteee", "rteee")
    auxid = aux["Id"] 

    gidaux = add_match_db("5", "5", auxid)
    gidauxid = gidaux["Match_id"]

    trash = 666

    response = client.get(
        f"/game/{trash}"
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "this match does not exist"}

def test_gamestatus_empty_mid():
    delete_data(Board)
    delete_data(Player)
    delete_data(Match)
    delete_data(User)

    create_user("rt@gmail.com", "rteee", "rteee")
    aux = get_user("rteee", "rteee")
    auxid = aux["Id"] 

    gidaux = add_match_db("5", "5", auxid)
    gidauxid = gidaux["Match_id"]

    response = client.get(
        f"/game/"
    )

    assert response.status_code == 404
    assert response.json()['detail'] == "Not Found" 
