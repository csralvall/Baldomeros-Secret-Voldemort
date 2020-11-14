from fastapi.testclient import TestClient

from server.db.crud import *
from server.tests.helpers import *

from server.main import app

client = TestClient(app)

def test_vote_avada_kedavra():
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
    pid = match['Player_id']    
    make_director(pid)
    set_current_director(match_id,0)

    add_user_in_match(uid2, match_id, 2)

    response = client.patch(
        f"/game/{match_id}/board/avada-kedavra?playername=bar"
    )

    assert response.status_code == 200
    assert response.json() == "bar is dead"

def test_vote_avada_kedavra_minister_autokill():
    delete_data(Board)
    delete_data(Player)
    delete_data(Match)
    delete_data(User)

    create_user("foo@gmail.com", "foo", "foo")
    create_user("bar@gmail.com", "bar", "bar")
    uid1 = get_user("foo", "foo")["Id"]
    uid2 = get_user("bar", "bar")["Id"]

    match_id = add_match_db(5,7,uid1)['Match_id']

    add_user_in_match(uid2, match_id, 2)

    set_gob_roles(match_id)

    minister = get_minister_username(match_id)

    response = client.patch(
        f"/game/{match_id}/board/avada-kedavra?playername={minister}"
    )

    assert response.status_code == 403
    assert response.json()['detail'] == "You can't kill yourself"

def test_vote_avada_kedavra_bad_playername():
    delete_data(Board)
    delete_data(Player)
    delete_data(Match)
    delete_data(User)

    create_user("foo@gmail.com", "foo", "foo")
    uid1 = get_user("foo", "foo")["Id"]

    match_id = add_match_db(5,7,uid1)['Match_id']

    response = client.patch(
        f"/game/{match_id}/board/avada-kedavra?playername=asdad"
    )

    assert response.status_code == 404
    assert response.json()['detail'] == "Resource not found"

def test_vote_avada_kedavra_bad_match_id():
    delete_data(Board)
    delete_data(Player)
    delete_data(Match)
    delete_data(User)

    create_user("foo@gmail.com", "foo", "foo")
    create_user("bar@gmail.com", "bar", "bar")
    uid1 = get_user("foo", "foo")["Id"]
    uid2 = get_user("bar", "bar")["Id"]

    match_id = add_match_db(5,7,uid1)['Match_id']

    add_user_in_match(uid2, match_id, 2)

    match_id += 1

    response = client.patch(
        f"/game/{match_id}/board/avada-kedavra?playername=bar"
    )

    assert response.status_code == 404
    assert response.json()['detail'] == "Match not found"

def test_vote_avada_kedavra_empty_match_id():
    delete_data(Board)
    delete_data(Player)
    delete_data(Match)
    delete_data(User)

    response = client.patch(
        f"/game//board/avada-kedavra?playername=bar"
    )

    assert response.status_code == 404
    assert response.json()['detail'] == "Not Found"

def test_vote_avada_kedavra_char_match_id():
    delete_data(Board)
    delete_data(Player)
    delete_data(Match)
    delete_data(User)

    response = client.patch(
        f"/game/afda/board/avada-kedavra?playername=bar"
    )

    assert response.status_code == 422
    assert response.json()['detail'][0]['msg'] == "value is not a valid integer"

def test_vote_avada_kedavra_without_player_name():
    delete_data(Board)
    delete_data(Player)
    delete_data(Match)
    delete_data(User)

    response = client.patch(
        f"/game/123/board/avada-kedavra"
    )

    assert response.status_code == 422
    assert response.json()['detail'][0]['msg'] == "field required"


def test_vote_avada_kedavra_bad_player_name_field():
    delete_data(Board)
    delete_data(Player)
    delete_data(Match)
    delete_data(User)

    response = client.patch(
        f"/game/123/board/avada-kedavra?player=bar"
    )

    assert response.status_code == 422
    assert response.json()['detail'][0]['msg'] == "field required"


def test_vote_avada_kedavra_empty_player_name_field():
    delete_data(Board)
    delete_data(Player)
    delete_data(Match)
    delete_data(User)

    create_user("foo@gmail.com", "foo", "foo")
    uid1 = get_user("foo", "foo")["Id"]

    match_id = add_match_db(5,7,uid1)['Match_id']

    response = client.patch(
        f"/game/{match_id}/board/avada-kedavra?playername="
    )

    assert response.status_code == 404
    assert response.json()['detail'] == "Resource not found"


