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

def test_vote_avada_kedavra_voldemort_kill():
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

    bar_player_id = get_player_id(match_id, uid2)

    change_player_rol(pid, PHOENIX)
    change_player_rol(bar_player_id, VOLDEMORT)

    response = client.patch(
        f"/game/{match_id}/board/avada-kedavra?playername=bar"
    )

    assert response.status_code == 200
    assert response.json() == "bar is dead"
    assert check_winner(match_id) == PHOENIX_STR
    assert get_match_status(match_id) == Status[FINISHED]

def test_vote_avada_kedavra_voldemort_not_set():
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

    bar_player_id = get_player_id(match_id, uid2)

    change_player_rol(pid, PHOENIX)
    change_player_rol(bar_player_id, PHOENIX)

    response = client.patch(
        f"/game/{match_id}/board/avada-kedavra?playername=bar"
    )

    assert response.status_code == 500
    assert response.json()['detail'] == "Voldemort was not set"

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

def test_expelliarmus_bad_match_id():
    delete_data(Board)
    delete_data(Player)
    delete_data(Match)
    delete_data(User)

    response = client.patch(
        f"/game/{-1}/board/expelliarmus?playername=adad"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "this match does not exist"

def test_expelliarmus_bad_playername():
    delete_data(Board)
    delete_data(Player)
    delete_data(Match)
    delete_data(User)

    create_user("foo@gmail.com", "foo", "foo")
    user_id = get_user("foo", "foo")["Id"]

    match_id = add_match_db(5,7,user_id)['Match_id']

    response = client.patch(
        f"/game/{match_id}/board/expelliarmus?playername=bar"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Player not found"

def test_expelliarmus_director_call():
    delete_data(Board)
    delete_data(Player)
    delete_data(Match)
    delete_data(User)

    create_user("foo@gmail.com", "foo", "foo")
    user_id = get_user("foo", "foo")["Id"]

    match_id = add_match_db(5,7,user_id)['Match_id']

    board_id = get_match_board_id(match_id)

    for i in range(5):
        enact_proclamation(match_id, DEATH_EATER_STR)

    unlock_expelliarmus(board_id)

    player_id = get_player_id(match_id, user_id)

    make_director(player_id)
    set_current_director(match_id, 0)
    director = get_director_username(match_id)

    response = client.patch(
        f"/game/{match_id}/board/expelliarmus?playername={director}"
    )

    assert response.status_code == 200
    assert get_expelliarmus_status(board_id) == expelliarmus[MINISTER_STAGE]
    assert get_ingame_status(match_id) == ingame_status[EXPELLIARMUS]

def test_expelliarmus_director_call_expelliarmus_locked():
    delete_data(Board)
    delete_data(Player)
    delete_data(Match)
    delete_data(User)

    create_user("foo@gmail.com", "foo", "foo")
    user_id = get_user("foo", "foo")["Id"]

    match_id = add_match_db(5,7,user_id)['Match_id']

    player_id = get_player_id(match_id, user_id)

    make_director(player_id)
    set_current_director(match_id, 0)
    director = get_director_username(match_id)

    response = client.patch(
        f"/game/{match_id}/board/expelliarmus?playername={director}"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Not allowed."

def test_expelliarmus_minister_call():
    delete_data(Board)
    delete_data(Player)
    delete_data(Match)
    delete_data(User)

    create_user("foo@gmail.com", "foo", "foo")
    create_user("bar@gmail.com", "bar", "bar")
    user_id = get_user("foo", "foo")["Id"]
    user_id2 = get_user("bar", "bar")["Id"]

    match_id = add_match_db(5,7,user_id)['Match_id']
    board_id = get_match_board_id(match_id)

    add_user_in_match(user_id2, match_id, 2)


    for i in range(5):
        enact_proclamation(match_id, DEATH_EATER_STR)

    unlock_expelliarmus(board_id)

    player_id = get_player_id(match_id, user_id)
    player_id2 = get_player_id(match_id, user_id2)

    make_minister(player_id)
    minister = get_minister_username(match_id)

    make_director(player_id2)
    set_current_director(match_id, 0)
    director = get_director_username(match_id)

    set_expelliarmus_status(board_id, MINISTER_STAGE)

    create_deck(board_id)
    get_top_three_proclamation(board_id)
    get_selected_card(board_id)

    response = client.patch(
        f"/game/{match_id}/board/expelliarmus?playername={minister}&minister-desition=expelliarmus"
    )

    assert response.status_code == 200
    assert get_ingame_status(match_id) == ingame_status[NOMINATION]
    assert get_expelliarmus_status(board_id) == expelliarmus[UNLOCKED]

def test_expelliarmus_minister_call_no_minister_stage():
    delete_data(Board)
    delete_data(Player)
    delete_data(Match)
    delete_data(User)

    create_user("foo@gmail.com", "foo", "foo")
    create_user("bar@gmail.com", "bar", "bar")
    user_id = get_user("foo", "foo")["Id"]
    user_id2 = get_user("bar", "bar")["Id"]

    match_id = add_match_db(5,7,user_id)['Match_id']
    board_id = get_match_board_id(match_id)

    add_user_in_match(user_id2, match_id, 2)

    for i in range(5):
        enact_proclamation(match_id, DEATH_EATER_STR)

    unlock_expelliarmus(board_id)

    player_id = get_player_id(match_id, user_id)
    player_id2 = get_player_id(match_id, user_id2)

    make_minister(player_id)
    minister = get_minister_username(match_id)

    make_director(player_id2)
    set_current_director(match_id, 0)
    director = get_director_username(match_id)

    set_expelliarmus_status(board_id, UNLOCKED)

    create_deck(board_id)
    get_top_three_proclamation(board_id)
    get_selected_card(board_id)

    response = client.patch(
        f"/game/{match_id}/board/expelliarmus?playername={minister}&minister-desition=expelliarmus"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "No desition to make."

def test_expelliarmus_minister_call_minister_desition_none():
    delete_data(Board)
    delete_data(Player)
    delete_data(Match)
    delete_data(User)

    create_user("foo@gmail.com", "foo", "foo")
    create_user("bar@gmail.com", "bar", "bar")
    user_id = get_user("foo", "foo")["Id"]
    user_id2 = get_user("bar", "bar")["Id"]

    match_id = add_match_db(5,7,user_id)['Match_id']
    board_id = get_match_board_id(match_id)

    add_user_in_match(user_id2, match_id, 2)

    for i in range(5):
        enact_proclamation(match_id, DEATH_EATER_STR)

    unlock_expelliarmus(board_id)

    player_id = get_player_id(match_id, user_id)
    player_id2 = get_player_id(match_id, user_id2)

    make_minister(player_id)
    minister = get_minister_username(match_id)

    make_director(player_id2)
    set_current_director(match_id, 0)
    director = get_director_username(match_id)

    set_expelliarmus_status(board_id, MINISTER_STAGE)

    create_deck(board_id)
    get_top_three_proclamation(board_id)
    get_selected_card(board_id)

    response = client.patch(
        f"/game/{match_id}/board/expelliarmus?playername={minister}"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Minister must decide."

def test_expelliarmus_minister_not_discarded_proclamation():
    delete_data(Board)
    delete_data(Player)
    delete_data(Match)
    delete_data(User)

    create_user("foo@gmail.com", "foo", "foo")
    create_user("bar@gmail.com", "bar", "bar")
    user_id = get_user("foo", "foo")["Id"]
    user_id2 = get_user("bar", "bar")["Id"]

    match_id = add_match_db(5,7,user_id)['Match_id']
    board_id = get_match_board_id(match_id)

    add_user_in_match(user_id2, match_id, 2)

    for i in range(5):
        enact_proclamation(match_id, DEATH_EATER_STR)

    unlock_expelliarmus(board_id)

    player_id = get_player_id(match_id, user_id)
    player_id2 = get_player_id(match_id, user_id2)

    make_minister(player_id)
    minister = get_minister_username(match_id)

    make_director(player_id2)
    set_current_director(match_id, 0)
    director = get_director_username(match_id)

    set_expelliarmus_status(board_id, MINISTER_STAGE)

    create_deck(board_id)
    get_top_three_proclamation(board_id)

    response = client.patch(
        f"/game/{match_id}/board/expelliarmus?playername={minister}&minister-desition=expelliarmus"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Minister should discard one card."

