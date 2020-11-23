from fastapi.testclient import TestClient

from server.db.crud import *
from server.tests.helpers import *

from server.main import app

client = TestClient(app)

def test_match_not_exist():
    delete_data(Board)
    delete_data(Player)
    delete_data(Match)
    delete_data(User)

    pid = 1
    mid = 1

    response = client.patch(
        f"/game/{mid}/leave/{pid}"
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
    mid = match['Match_id']
    pid = 99999

    response = client.patch(
        f"/game/{mid}/leave/{pid}"
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
    mid = match['Match_id']
    pid = match['Player_id']
    
    change_match_status(mid, IN_GAME):

    response = client.patch(
        f"/game/{mid}/leave/{pid}"
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "game already started"}

def test_leave_game_OK():
    delete_data(Board)
    delete_data(Player)
    delete_data(Match)
    delete_data(User)

    create_user("foo@gmail.com", "foo", "foo")
    create_user("bar@gmail.com", "bar", "bar")
    uid1 = get_user("foo", "foo")["Id"]
    uid2 = get_user("bar", "bar")["Id"]

    match = add_match_db(5,7,uid1)
    mid = match['Match_id']
    pid = match['Player_id']

    playername = get_player_username(pid)

    response = client.patch(
        f"/game/{mid}/leave/{pid}"
    )

    assert response.status_code == 200
    assert response.json() == f"{playername} is not longer in the game"