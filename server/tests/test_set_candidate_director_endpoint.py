
from fastapi.testclient import TestClient

from server.db.crud import *
from server.tests.helpers import *

from server.main import app

client = TestClient(app)

def test_select_candidate_Player_not_exist():
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
    pid = 3

    response = client.patch(
        f"/game/{mid}/director/{pid}"
    )

    assert response.status_code == 404
    assert response.json()['detail'] == "Player not found"

def test_select_candidate_Match_not_exist():
    delete_data(Board)
    delete_data(Player)
    delete_data(Match)
    delete_data(User)

    create_user("foo@gmail.com", "foo", "foo")
    create_user("bar@gmail.com", "bar", "bar")
    uid1 = get_user("foo", "foo")["Id"]
    uid2 = get_user("bar", "bar")["Id"]

    match = add_match_db(5,7,uid1)
    pid = 1
    mid = 99

    response = client.patch(
        f"/game/{mid}/director/{pid}"
    )

    assert response.status_code == 404
    assert response.json()['detail'] == "Match not found"

def test_select_candidate_resource_not_found():
    delete_data(Board)
    delete_data(Player)
    delete_data(Match)
    delete_data(User)

    create_user("foo@gmail.com", "foo", "foo")
    create_user("bar@gmail.com", "bar", "bar")
    create_user("m@gmail.com", "m", "m")
    uid1 = get_user("foo", "foo")["Id"]
    uid2 = get_user("bar", "bar")["Id"]
    uid3 = get_user("m", "m")["Id"]

    match = add_match_db(5,7,uid1)
    mid = match['Match_id']
    pid2 = add_user_in_match(uid2, mid, 2).PlayerId
    match2 = add_match_db(5,7,uid3)
    pid3 = 3 #playerid uid3 in match2

    response = client.patch(
        f"/game/{mid}/director/{pid3}"
    )

    assert response.status_code == 404
    assert response.json()['detail'] == "Player not found"

def test_select_candidate_t():
    delete_data(Board)
    delete_data(Player)
    delete_data(Match)
    delete_data(User)

    create_user("foo@gmail.com", "foo", "foo")
    create_user("bar@gmail.com", "bar", "bar")
    create_user("m@gmail.com", "m", "m")
    uid1 = get_user("foo", "foo")["Id"]
    uid2 = get_user("bar", "bar")["Id"]

    match = add_match_db(5,7,uid1)
    mid = match['Match_id']
    pid2 = add_user_in_match(uid2, mid, 2).PlayerId

    response = client.patch(
        f"/game/{mid}/director/{pid2}"
    )

    assert response.status_code == 200
    assert response.json() == "bar is the candidate to director"
