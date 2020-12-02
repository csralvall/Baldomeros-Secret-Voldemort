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


from server.tests.helpers import *

from server.main import app

client = TestClient(app)


def test_create_match_ok():
    delete_data(Board)
    delete_data(Player)
    delete_data(Match)
    delete_data(User)
    create_user("rt@gmail.com", "rteee", "rteee")
    aux = get_user("rteee", "rteee")
    auxid = aux["Id"] 
    response = client.post(
        f"/game/new?minp=5&maxp=5&uhid={auxid}"
    )

    assert response.status_code == 200
    assert response.json()["Match_id"] is not None
    assert response.json()["Player_id"] is not None

def test_create_match_minp_bigger_than_maxp():
    delete_data(Board)
    delete_data(Player)
    delete_data(Match)
    delete_data(User)
    create_user("rt@gmail.com", "rteee", "rteee")     
    aux = get_user("rteee", "rteee")
    auxid = aux["Id"]  
    response = client.post(
        f"/game/new?minp=7&maxp=5&uhid={auxid}"
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "couldnt create the game"}     

def test_create_match_empty_minp():
    delete_data(Board)
    delete_data(Player)
    delete_data(Match)
    delete_data(User)
    create_user("rt@gmail.com", "rteee", "rteee")     
    aux = get_user("rteee", "rteee")
    auxid = aux["Id"]  
    response = client.post(
        f"/game/new?maxp=5&uhid={auxid}"
    )

    assert response.status_code == 422
    assert response.json() == {'detail': [{'loc': ['query', 'minp'], 'msg': 'field required', 'type': 'value_error.missing'}]}        

def test_create_match_empty_user():
    delete_data(Board)
    delete_data(Player)
    delete_data(Match)
    delete_data(User)

    response = client.post(
        "/game/new?minp=7&maxp=5"
    )

    assert response.status_code == 422
    assert response.json()['detail'][0]['msg'] == "field required"   

def test_create_match_empty_maxp():

    delete_data(Board)
    delete_data(Player)
    delete_data(Match)
    delete_data(User)
    create_user("rt@gmail.com", "rteee", "rteee")     
    aux = get_user("rteee", "rteee")
    auxid = aux["Id"]  
    response = client.post(
        f"/game/new?minp=7&uhid={auxid}"
    )

    assert response.status_code == 422
    assert response.json()['detail'][0]['msg'] == "field required"   

def test_create_match_minp_min_shouldbe5():

    delete_data(Board)
    delete_data(Player)
    delete_data(Match)
    delete_data(User)
    create_user("rt@gmail.com", "rteee", "rteee")     
    aux = get_user("rteee", "rteee")
    auxid = aux["Id"]  
    response = client.post(
        f"/game/new?minp=4&maxp=5&uhid={auxid}"
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "couldnt create the game"}   

def test_create_match_maxp_max_shouldbe10():

    delete_data(Board)
    delete_data(Player)
    delete_data(Match)
    delete_data(User)
    create_user("rt@gmail.com", "rteee", "rteee")     
    aux = get_user("rteee", "rteee")
    auxid = aux["Id"]  
    response = client.post(
        f"/game/new?minp=5&maxp=11&uhid={auxid}"
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "couldnt create the game"}                     

