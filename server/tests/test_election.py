from fastapi.testclient import TestClient

from server.db.crud import *
from server.tests.helpers import *

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
    set_candidate_director_test(gid,0)
    make_director(pid)
    set_current_director(gid,0)

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

    make_director(pid)
    set_candidate_director_test(gid,0)
    set_current_director(gid,0)

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
    bid = get_match_board_id(gid)
    create_deck(bid)
    shuffle_deck(bid)
    get_top_three_proclamation(bid)


    add_user_in_match(baruid,gid,1)
    add_user_in_match(bazuid,gid,2)
    add_user_in_match(zoouid,gid,3)
    add_user_in_match(zaruid,gid,4)

    pid = get_player_id(gid,uid)
    barpid = get_player_id(gid,baruid)
    bazpid = get_player_id(gid,bazuid)
    zoopid = get_player_id(gid,zoouid)
    zarpid = get_player_id(gid,zaruid)

    name_list = ['foo','bar','baz','zoo','zar']

    make_minister(zoopid)
    set_current_minister(gid,3)
    i=0
    for p in name_list:
        change_ingame_status(gid, ELECTION)
        set_next_candidate_director(gid,i)
        assert get_candidate_director_username(gid)== p
        restore_election(gid)
        
        client.put(f"/game/{gid}/player/{pid}?vote=lumos")
        assert get_candidate_director_username(gid)== p 
        client.put(f"/game/{gid}/player/{barpid}?vote=lumos")
        assert get_candidate_director_username(gid)== p 
        client.put(f"/game/{gid}/player/{bazpid}?vote=lumos")
        assert get_candidate_director_username(gid)== p 
        client.put(f"/game/{gid}/player/{zoopid}?vote=lumos")
        assert get_candidate_director_username(gid)== p 
        client.put(f"/game/{gid}/player/{zarpid}?vote=lumos")
        assert get_director_username(gid) == p
        assert get_ingame_status(gid) == ingame_status[MINISTER_SELECTION]
        change_to_exdirector(gid)
        i=i+1

    i=0
    for p in name_list:
        change_ingame_status(gid, ELECTION)
        set_next_candidate_director(gid,i)
        assert get_candidate_director_username(gid)== p
        restore_election(gid)
        client.put(f"/game/{gid}/player/{pid}?vote=nox")
        assert get_candidate_director_username(gid)== p 
        client.put(f"/game/{gid}/player/{barpid}?vote=nox")
        assert get_candidate_director_username(gid)== p 
        client.put(f"/game/{gid}/player/{bazpid}?vote=nox")
        assert get_candidate_director_username(gid)== p 
        client.put(f"/game/{gid}/player/{zoopid}?vote=nox")
        assert get_candidate_director_username(gid)== p 
        client.put(f"/game/{gid}/player/{zarpid}?vote=nox")
        assert get_director_username(gid) == "No director yet"
        assert get_ingame_status(gid) == ingame_status[NOMINATION]#cuando agreguemos el ingame status chaos, va a fallar
        i=i+1
        assert get_failed_election_count(bid)== i % 3
        assert i//3 == get_phoenix_proclamations(gid)+ get_death_eater_proclamations(gid)

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
    bid = get_match_board_id(gid)
    create_deck(bid)
    shuffle_deck(bid)
    get_top_three_proclamation(bid)

    add_user_in_match(baruid,gid,1)
    add_user_in_match(bazuid,gid,2)
    add_user_in_match(zoouid,gid,3)
    add_user_in_match(zaruid,gid,4)

    pid = get_player_id(gid,uid)
    barpid = get_player_id(gid,baruid)
    bazpid = get_player_id(gid,bazuid)
    zoopid = get_player_id(gid,zoouid)
    zarpid = get_player_id(gid,zaruid)

    name_list = ['foo','bar','baz','zoo','zar']

    enact_proclamation(gid,"death eater")
    enact_proclamation(gid,"death eater")
    enact_proclamation(gid,"death eater")

    make_minister(zoopid)
    set_current_minister(gid,3)

    change_ingame_status(gid, ELECTION)

    make_voldemort(pid)
    set_next_candidate_director(gid,0)
    restore_election(gid)
    
    client.put(f"/game/{gid}/player/{pid}?vote=lumos")
    client.put(f"/game/{gid}/player/{barpid}?vote=lumos")
    client.put(f"/game/{gid}/player/{bazpid}?vote=lumos")
    client.put(f"/game/{gid}/player/{zoopid}?vote=lumos")
    client.put(f"/game/{gid}/player/{zarpid}?vote=lumos")
    assert check_winner(gid) == DEATH_EATER_WINNER
    assert get_ingame_status(gid) == ingame_status[MINISTER_SELECTION]

