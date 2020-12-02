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

def test_match_not_exist():
    delete_data(Board)
    delete_data(Player)
    delete_data(Match)
    delete_data(User)

    player_id = 1
    match_id = 1

    response = client.patch(
        f"/game/{match_id}/leave/{player_id}"
    )

    assert response.status_code == 404
    assert response.json() == {"detail":"this match does not exist"}

def test_player_not_in_match():
    delete_data(Board)
    delete_data(Player)
    delete_data(Match)
    delete_data(User)

    create_user("foo@gmail.com", "foo", "foo")
    create_user("bar@gmail.com", "bar", "bar")
    uid1 = get_user("foo", "foo")["Id"]
    uid2 = get_user("bar", "bar")["Id"]

    match = add_match_db(5,7,uid1)
    match_id = match['Match_id']
    player_id = 99999

    response = client.patch(
        f"/game/{match_id}/leave/{player_id}"
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Player not found"}

def test_match_already_started():
    delete_data(Board)
    delete_data(Player)
    delete_data(Match)
    delete_data(User)

    create_user("foo@gmail.com", "foo", "foo")
    create_user("bar@gmail.com", "bar", "bar")
    uid1 = get_user("foo", "foo")["Id"]
    uid2 = get_user("bar", "bar")["Id"]

    match = add_match_db(5,7,uid1)
    match_id = match['Match_id']
    player_id = match['Player_id']
    
    change_match_status(match_id, IN_GAME)

    response = client.patch(
        f"/game/{match_id}/leave/{player_id}"
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "game already started"}

def test_leave_game_creator_OK():
    delete_data(Board)
    delete_data(Player)
    delete_data(Match)
    delete_data(User)

    create_user("foo@gmail.com", "foo", "foo")
    create_user("bar@gmail.com", "bar", "bar")
    uid1 = get_user("foo", "foo")["Id"]
    uid2 = get_user("bar", "bar")["Id"]

    match = add_match_db(5,7,uid1)
    match_id = match['Match_id']
    player_id = match['Player_id']

    response = client.patch(
        f"/game/{match_id}/leave/{player_id}"
    )

    assert response.status_code == 200
    assert response.json() == "the game is over, the creator left the game"
    assert get_match_status(match_id) == "Closed"

def test_leave_game_not_creator_OK():
    delete_data(Board)
    delete_data(Player)
    delete_data(Match)
    delete_data(User)

    create_user("foo@gmail.com", "foo", "foo")
    create_user("bar@gmail.com", "bar", "bar")
    uid1 = get_user("foo", "foo")["Id"]
    uid2 = get_user("bar", "bar")["Id"]

    match = add_match_db(5,7,uid1)
    match_id = match['Match_id']
    add_user_in_match(uid2, match_id, 1)

    player_id = get_player_id(match_id, uid2)

    playername = get_player_username(player_id)

    response = client.patch(
        f"/game/{match_id}/leave/{player_id}"
    )

    assert response.status_code == 200
    assert response.json() == f"{playername} is not longer in the game" 