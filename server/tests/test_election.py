from fastapi.testclient import TestClient

from server.db.crud import *

from server.main import app

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

def test_vote_endpoint():
    delete_data(Board)
    delete_data(Player)
    delete_data(Match)
    delete_data(User)

    create_user("foo@gmail.com", "foo", "foo")
    create_user("baz@gmail.com", "baz", "baz")
    create_user("bar@gmail.com", "bar", "bar")
    create_user("zoo@gmail.com", "zoo", "zoo")
    create_user("zar@gmail.com", "zar", "zar")
    user = get_user("foo", "foo")
    baruid = get_user("bar", "bar")['Id']
    bazuid = get_user("baz", "baz")['Id']
    zoouid = get_user("zoo", "zoo")['Id']
    zaruid = get_user("zar", "zar")['Id']
    uid = user['Id']

    gid = add_match_db(5,7,uid)['Match_id']

    add_user_in_match(baruid,gid,1)
    add_user_in_match(bazuid,gid,2)
    add_user_in_match(zoouid,gid,3)
    add_user_in_match(zaruid,gid,4)

    pid = get_player_id(gid,uid)
    barpid = get_player_id(gid,baruid)
    bazpid = get_player_id(gid,bazuid)
    zoopid = get_player_id(gid,zoouid)
    zarpid = get_player_id(gid,zaruid)

    name_list = ['bar','baz','zoo','zar','foo']

    for p in name_list:
        client.put(f"/game/{gid}/player/{pid}?vote=lumos")
        client.put(f"/game/{gid}/player/{barpid}?vote=lumos")
        client.put(f"/game/{gid}/player/{bazpid}?vote=lumos")
        client.put(f"/game/{gid}/player/{zoopid}?vote=lumos")
        client.put(f"/game/{gid}/player/{zarpid}?vote=lumos")

        assert get_minister_username(gid) == p

    for p in name_list:
        client.put(f"/game/{gid}/player/{pid}?vote=nox")
        client.put(f"/game/{gid}/player/{barpid}?vote=nox")
        client.put(f"/game/{gid}/player/{bazpid}?vote=nox")
        client.put(f"/game/{gid}/player/{zoopid}?vote=nox")
        client.put(f"/game/{gid}/player/{zarpid}?vote=nox")

        assert get_minister_username(gid) == p


def test_vote_endpoint_with_proclamations():
    delete_data(Board)
    delete_data(Player)
    delete_data(Match)
    delete_data(User)

    create_user("foo@gmail.com", "foo", "foo")
    create_user("baz@gmail.com", "baz", "baz")
    create_user("bar@gmail.com", "bar", "bar")
    create_user("zoo@gmail.com", "zoo", "zoo")
    create_user("zar@gmail.com", "zar", "zar")
    user = get_user("foo", "foo")
    baruid = get_user("bar", "bar")['Id']
    bazuid = get_user("baz", "baz")['Id']
    zoouid = get_user("zoo", "zoo")['Id']
    zaruid = get_user("zar", "zar")['Id']
    uid = user['Id']

    gid = add_match_db(5,7,uid)['Match_id']

    add_user_in_match(baruid,gid,1)
    add_user_in_match(bazuid,gid,2)
    add_user_in_match(zoouid,gid,3)
    add_user_in_match(zaruid,gid,4)

    pid = get_player_id(gid,uid)
    barpid = get_player_id(gid,baruid)
    bazpid = get_player_id(gid,bazuid)
    zoopid = get_player_id(gid,zoouid)
    zarpid = get_player_id(gid,zaruid)

    name_list = ['bar','baz','zoo','zar','foo']

    for i in range(0,6):
        client.put(f"/game/{gid}/player/{pid}?vote=lumos")
        client.put(f"/game/{gid}/player/{barpid}?vote=lumos")
        client.put(f"/game/{gid}/player/{bazpid}?vote=lumos")
        client.put(f"/game/{gid}/player/{zoopid}?vote=lumos")
        client.put(f"/game/{gid}/player/{zarpid}?vote=lumos")

    assert is_victory_from(gid) == 'death eater'
    assert get_match_status(gid) == 'Finished'


