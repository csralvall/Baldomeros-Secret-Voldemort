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
    bid = get_match_board_id(gidauxid)
    create_deck(bid)

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

    
def test_gamestatus_ok_2():
    delete_data(Board)
    delete_data(Player)
    delete_data(Match)
    delete_data(User)

    create_user("rt@gmail.com", "rteee", "rteee")
    aux = get_user("rteee", "rteee")
    auxid = aux["Id"] 
    username = "rteee"
    message = "hola"
    match = add_match_db("5", "5", auxid)
    matchid = match["Match_id"]
    bid = get_match_board_id(matchid)
    create_deck(bid)
    send_message(matchid,username, message)

    response = client.get(
        f"/game/{matchid}"
    )

    assert response.status_code == 200
    assert response.json() == {'boardstatus':
                                {'boardtype': '5-6', 'deatheaterproclamations': 0, 'expelliarmus': 'locked',
                                 'failcounter': 0,'phoenixproclamations': 0,'spell': None,'status': 'nomination'},
                                 'candidate':'No director candidate yet', 'chat': {'0': {'Text': 'hola', 'Username': 'rteee'}},
                                 'director': 'No director yet','hand': [],'matchstatus': 'Joinable', 'minister': 'rteee',
                                'playerstatus': {'rteee': {'isDead': False, 'vote': 'missing vote'}}, 'winner': 'no winner yet'}
