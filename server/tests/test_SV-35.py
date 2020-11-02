from fastapi.testclient import TestClient

from server.db.crud import *

from server.main import app

client = TestClient(app)

def test_join_match_ok():
    delete_data(Board)
    delete_data(Player)
    delete_data(Match)
    delete_data(User)

    create_user("rt@gmail.com", "rteee", "rteee")
    aux = get_user("rteee", "rteee")
    auxid = aux["Id"] 

    gidaux = add_match_db("5", "5", auxid)
    gidauxid = gidaux["Match_id"]

    create_user("rt2@gmail.com", "rteee2", "rteee2")
    aux2 = get_user("rteee2", "rteee2")
    auxid2 = aux2["Id"] 

    response = client.post(
        f"/game/{gidauxid}?user={auxid2}"
    )

    assert response.status_code == 200
    assert response.json()["Match_id"] is not None
    assert response.json()["Player_id"] is not None

def test_join_match_fail_mid():
    delete_data(Board)
    delete_data(Player)
    delete_data(Match)
    delete_data(User)

    create_user("rt@gmail.com", "rteee", "rteee")
    aux = get_user("rteee", "rteee")
    auxid = aux["Id"] 

    trash = 666

    response = client.post(
        f"/game/{trash}?user={auxid}" 
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "there is no space"}

def test_join_match_fail_user():
    delete_data(Board)
    delete_data(Player)
    delete_data(Match)
    delete_data(User)

    create_user("rt@gmail.com", "rteee", "rteee")
    aux = get_user("rteee", "rteee")
    auxid = aux["Id"] 

    gidaux = add_match_db("5", "5", auxid)
    gidauxid = gidaux["Match_id"]

    response = client.post(
        f"/game/{gidauxid}?&user=666"
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "couldnt add the user"}

def test_join_match_empty_mid():
    delete_data(Board)
    delete_data(Player)
    delete_data(Match)
    delete_data(User)

    create_user("rt@gmail.com", "rteee", "rteee")
    aux = get_user("rteee", "rteee")
    auxid = aux["Id"] 

    response = client.post(
        f"/game/?user={auxid}" 
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Not Found"}

def test_join_match_empty_user():
    delete_data(Board)
    delete_data(Player)
    delete_data(Match)
    delete_data(User)

    create_user("rt@gmail.com", "rteee", "rteee")
    aux = get_user("rteee", "rteee")
    auxid = aux["Id"] 

    gidaux = add_match_db("5", "5", auxid)
    gidauxid = gidaux["Match_id"]

    response = client.post(
        f"/game/{gidauxid}" 
    )

    assert response.status_code == 422
    assert response.json()['detail'][0]['msg'] == "field required"    
