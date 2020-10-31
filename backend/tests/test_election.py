from fastapi.testclient import TestClient

from backend.db.crud import *

from backend.main import app

client = TestClient(app)

def test_vote_nox():
    delete_data(Board)
    delete_data(Player)
    delete_data(Match)
    delete_data(User)

    create_user("foo@gmail.com", "foo", "foo")
    user = get_user("foo", "foo")
    uid = user['Id']

    gid = add_match_db(5,7,uid)['Match_id']

    pid = get_player_id(gid,uid)

    response = client.put(
        f"/game/{gid}/player/{pid}?vote=nox",
    )

    assert response.status_code == 200
    assert response.json() == get_player_votes(gid)['foo']

def test_vote_lumos():
    delete_data(Board)
    delete_data(Player)
    delete_data(Match)
    delete_data(User)

    create_user("foo@gmail.com", "foo", "foo")
    user = get_user("foo", "foo")
    uid = user['Id']

    gid = add_match_db(5,7,uid)['Match_id']

    pid = get_player_id(gid,uid)

    response = client.put(
        f"/game/{gid}/player/{pid}?vote=lumos",
    )

    assert response.status_code == 200
    assert response.json() == get_player_votes(gid)['foo']

def test_vote_negative_match_id():
    delete_data(Board)
    delete_data(Player)
    delete_data(Match)
    delete_data(User)

    create_user("foo@gmail.com", "foo", "foo")
    user = get_user("foo", "foo")
    uid = user['Id']

    gid = add_match_db(5,7,uid)['Match_id']

    pid = get_player_id(gid,uid)

    response = client.put(
        f"/game/-1/player/{pid}?vote=nox",
    )

    assert response.status_code == 404
    assert response.json()['detail'] == "Match not found"

def test_vote_zero_match_id():
    delete_data(Board)
    delete_data(Player)
    delete_data(Match)
    delete_data(User)

    create_user("foo@gmail.com", "foo", "foo")
    user = get_user("foo", "foo")
    uid = user['Id']

    gid = add_match_db(5,7,uid)['Match_id']

    pid = get_player_id(gid,uid)

    response = client.put(
        f"/game/0/player/{pid}?vote=nox",
    )

    assert response.status_code == 404
    assert response.json()['detail'] == "Match not found"

def test_vote_player_from_another_match():
    delete_data(Board)
    delete_data(Player)
    delete_data(Match)
    delete_data(User)

    create_user("foo@gmail.com", "foo", "foo")
    user = get_user("foo", "foo")
    uid1 = user['Id']

    gid1 = add_match_db(5,7,uid1)['Match_id']

    pid1 = get_player_id(gid1,uid1)

    create_user("baz@gmail.com", "baz", "baz")
    user = get_user("baz", "baz")
    uid2 = user['Id']

    gid2 = add_match_db(5,7,uid2)['Match_id']

    pid2 = get_player_id(gid2,uid2)

    response = client.put(
        f"/game/{gid2}/player/{pid1}?vote=nox",
    )

    assert response.status_code == 404
    assert response.json()['detail'] == "Player not found"

def test_vote_not_allowed_vote():
    delete_data(Board)
    delete_data(Player)
    delete_data(Match)
    delete_data(User)

    create_user("foo@gmail.com", "foo", "foo")
    user = get_user("foo", "foo")
    uid = user['Id']

    gid = add_match_db(5,7,uid)['Match_id']

    pid = get_player_id(gid,uid)

    response = client.put(
        f"/game/{gid}/player/{pid}?vote=sfda",
    )

    assert response.status_code == 200
    #assert response.json() == get_player_votes(gid)['foo']

def test_vote_not_allowed_vote():
    delete_data(Board)
    delete_data(Player)
    delete_data(Match)
    delete_data(User)

    create_user("foo@gmail.com", "foo", "foo")
    user = get_user("foo", "foo")
    uid = user['Id']

    gid = add_match_db(5,7,uid)['Match_id']

    pid = get_player_id(gid,uid)

    response = client.put(
        f"/game/{gid}/player/{pid}?vote=sfda",
    )

    assert response.status_code == 422
    #assert response.json() == get_player_votes(gid)['foo']

def test_vote_empty():
    delete_data(Board)
    delete_data(Player)
    delete_data(Match)
    delete_data(User)

    create_user("foo@gmail.com", "foo", "foo")
    user = get_user("foo", "foo")
    uid = user['Id']

    gid = add_match_db(5,7,uid)['Match_id']

    pid = get_player_id(gid,uid)

    response = client.put(
        f"/game/{gid}/player/{pid}?vote=",
    )

    assert response.status_code == 422
    assert response.json()['detail'][0]['msg'] == (
        'string does not match regex "^(nox|lumos)$"')

def test_vote_empty_match_id():
    delete_data(Board)
    delete_data(Player)
    delete_data(Match)
    delete_data(User)

    create_user("foo@gmail.com", "foo", "foo")
    user = get_user("foo", "foo")
    uid = user['Id']

    gid = add_match_db(5,7,uid)['Match_id']

    pid = get_player_id(gid,uid)

    response = client.put(
        f"/game//player/{pid}?vote=lumos",
    )

    assert response.status_code == 404
    assert response.json()['detail'] == 'Not Found'

def test_vote_not_number_player_id():
    delete_data(Board)
    delete_data(Player)
    delete_data(Match)
    delete_data(User)

    create_user("foo@gmail.com", "foo", "foo")
    user = get_user("foo", "foo")
    uid = user['Id']

    gid = add_match_db(5,7,uid)['Match_id']

    pid = get_player_id(gid,uid)

    response = client.put(
        f"/game/{gid}/player/xdf?vote=lumos",
    )

    assert response.status_code == 422
    assert response.json()['detail'][0]['msg'] == 'value is not a valid integer'

def test_vote_not_number_match_id():
    delete_data(Board)
    delete_data(Player)
    delete_data(Match)
    delete_data(User)

    create_user("foo@gmail.com", "foo", "foo")
    user = get_user("foo", "foo")
    uid = user['Id']

    gid = add_match_db(5,7,uid)['Match_id']

    pid = get_player_id(gid,uid)

    response = client.put(
        f"/game/xdf/player/{pid}?vote=lumos",
    )

    assert response.status_code == 422
    assert response.json()['detail'][0]['msg'] == 'value is not a valid integer'

def test_vote_empty_player_id():
    delete_data(Board)
    delete_data(Player)
    delete_data(Match)
    delete_data(User)

    create_user("foo@gmail.com", "foo", "foo")
    user = get_user("foo", "foo")
    uid = user['Id']

    gid = add_match_db(5,7,uid)['Match_id']

    pid = get_player_id(gid,uid)

    response = client.put(
        f"/game/{gid}/player/?vote=lumos",
    )

    assert response.status_code == 404
    assert response.json()['detail'] == 'Not Found'
