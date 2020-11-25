from fastapi.testclient import TestClient

from server.db.crud import *
from server.tests.helpers import *

from server.main import app

client = TestClient(app)


def test_receive_cards_minister_ok_no_winner():
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
    make_minister(pid)
    set_current_minister(match_id, 0)
    pid2 =add_user_in_match(uid2, match_id, 1).PlayerId
    bid = get_match_board_id(match_id)
    create_deck(bid)
    shuffle_deck(bid)
    get_top_three_proclamation(bid)

    make_director(pid2)
    set_current_director(match_id,1)

    change_ingame_status(match_id, MINISTER_SELECTION)

    hand_db = show_selected_deck(bid)
    discarted_db = hand_db[0]
    selected_db_1=hand_db[1]
    selected_db_2=hand_db[2]


    response = client.post(
        f"/game/{match_id}/proclamation/{pid}?discarded={discarted_db}",
        json=[selected_db_1,selected_db_2]
    )
    assert response.status_code == 200
    assert response.json() == "no winner yet"
    assert get_ingame_status(match_id) == ingame_status[DIRECTOR_SELECTION]

def test_receive_cards_minister_bad_status():
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
    make_minister(pid)
    set_current_minister(match_id, 0)
    pid2 =add_user_in_match(uid2, match_id, 1).PlayerId
    bid = get_match_board_id(match_id)
    create_deck(bid)
    shuffle_deck(bid)
    get_top_three_proclamation(bid)

    make_director(pid2)
    set_current_director(match_id,1)

    change_ingame_status(match_id, NOMINATION)

    hand_db = show_selected_deck(bid)
    discarted_db = hand_db[0]
    selected_db_1=hand_db[1]
    selected_db_2=hand_db[2]


    response = client.post(
        f"/game/{match_id}/proclamation/{pid}?discarded={discarted_db}",
        json=[selected_db_1,selected_db_2]
    )
    assert response.status_code == 404
    assert response.json()['detail'] == "We are not in the minister selection stage."


def test_receive_cards_minister_wrong_len_selected():
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
    make_minister(pid)
    set_current_minister(match_id, 0)
    pid2 =add_user_in_match(uid2, match_id, 1).PlayerId
    bid = get_match_board_id(match_id)
    create_deck(bid)
    shuffle_deck(bid)
    get_top_three_proclamation(bid)

    make_director(pid2)
    set_current_director(match_id,1)

    change_ingame_status(match_id, MINISTER_SELECTION)

    hand_db = show_selected_deck(bid)
    discarted_db = hand_db[0]
    selected_db_1=hand_db[1]

    response = client.post(
        f"/game/{match_id}/proclamation/{pid}?discarded={discarted_db}",
        json=[selected_db_1]
    )
    assert response.status_code == 404
    assert response.json()['detail']  == "The number of proclamation selected doesn't match the number of proclamations expected from minister."

def test_receive_cards_minister_wrong_selected_cards():
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
    make_minister(pid)
    set_current_minister(match_id, 0)
    pid2 =add_user_in_match(uid2, match_id, 1).PlayerId
    bid = get_match_board_id(match_id)
    create_deck(bid)
    shuffle_deck(bid)
    get_top_three_proclamation(bid)

    make_director(pid2)
    set_current_director(match_id,1)

    change_ingame_status(match_id, MINISTER_SELECTION)

    hand_db = show_selected_deck(bid)
    discarted_db = hand_db[0]
    selected_db_1=hand_db[1]
    selected_db_2=hand_db[2]

    if selected_db_1 == PHOENIX_STR:
        selected_db_1 = DEATH_EATER_STR
    else:
        selected_db_1=PHOENIX_STR

    response = client.post(
        f"/game/{match_id}/proclamation/{pid}?discarded={discarted_db}",
        json=[selected_db_1,selected_db_2]
    )
    assert response.status_code == 404
    assert response.json()['detail']  == "The proclamation selected doesn't match the proclamations passed."


def test_receive_cards_director_ok():
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
    make_minister(pid)
    set_current_minister(match_id, 0)
    pid2 =add_user_in_match(uid2, match_id, 1).PlayerId
    bid = get_match_board_id(match_id)
    create_deck(bid)
    shuffle_deck(bid)
    get_top_three_proclamation(bid)

    make_director(pid2)
    set_current_director(match_id,1)

    change_ingame_status(match_id, DIRECTOR_SELECTION)

    hand_db = show_selected_deck(bid)
    discarted_db = hand_db[0]
    selected_db_1=hand_db[1]
    selected_db_2=hand_db[2]

    discard_proclamation(bid, selected_db_2)
    assert get_minister_username(match_id)=="foo"

    response = client.post(
        f"/game/{match_id}/proclamation/{pid2}?discarded={discarted_db}",
        json=[selected_db_1]
    )
    assert response.status_code == 200
    assert response.json() == "no winner yet"
    assert get_ingame_status(match_id) == ingame_status[NOMINATION]

    if selected_db_1 == PHOENIX_STR:
        assert get_phoenix_proclamations(match_id) == 1
        assert get_death_eater_proclamations(match_id) == 0
    else:
        assert get_phoenix_proclamations(match_id) == 0
        assert get_death_eater_proclamations(match_id) == 1
    
    assert get_minister_username(match_id)=="bar"
    assert len(show_selected_deck(bid))==3


def test_receive_cards_director_ok_5players():
    delete_data(Board)
    delete_data(Player)
    delete_data(Match)
    delete_data(User)

    create_user("foo1@gmail.com", "bar1", "bar1")
    create_user("bar2@gmail.com", "bar2", "bar2")
    create_user("faa3@gmail.com", "bar3", "bar3")
    create_user("bar4@gmail.com", "bar4", "bar4")
    create_user("foo5@gmail.com", "bar5", "bar5")
    uid1 = get_user("bar1", "bar1")["Id"]
    uid2 = get_user("bar2", "bar2")["Id"]
    uid3 = get_user("bar3", "bar3")["Id"]
    uid4 = get_user("bar4", "bar4")["Id"]
    uid5 = get_user("bar5", "bar5")["Id"]

    match = add_match_db(5,7,uid1)
    match_id = match['Match_id']
    pid = match['Player_id']
    pid2 =add_user_in_match(uid2, match_id, 1).PlayerId
    pid3 =add_user_in_match(uid3, match_id, 3).PlayerId
    pid4 =add_user_in_match(uid4, match_id, 4).PlayerId
    pid5 =add_user_in_match(uid5, match_id, 5).PlayerId

    bid = get_match_board_id(match_id)
    create_deck(bid)
    shuffle_deck(bid)
    get_top_three_proclamation(bid)

    make_minister(pid)
    set_current_minister(match_id, 0)
    make_director(pid3)
    set_current_director(match_id,2)

    change_ingame_status(match_id, DIRECTOR_SELECTION)

    hand_db = show_selected_deck(bid)
    discarted_db = hand_db[0]
    selected_db_1=hand_db[1]
    selected_db_2=hand_db[2]

    discard_proclamation(bid, selected_db_2)
    assert get_minister_username(match_id)=="bar1"
    assert get_director_username(match_id)=="bar3"

    response = client.post(
        f"/game/{match_id}/proclamation/{pid3}?discarded={discarted_db}",
        json=[selected_db_1]
    )
    assert response.status_code == 200
    assert response.json() == "no winner yet"
    assert get_ingame_status(match_id) == ingame_status[NOMINATION]

    if selected_db_1 == PHOENIX_STR:
        assert get_phoenix_proclamations(match_id) == 1
        assert get_death_eater_proclamations(match_id) == 0
    else:
        assert get_phoenix_proclamations(match_id) == 0
        assert get_death_eater_proclamations(match_id) == 1
    
    assert get_minister_username(match_id)=="bar2"
    assert get_exdirector_username(match_id)=="bar3"
    assert len(show_selected_deck(bid))==3


def test_receive_cards_director_ok_winner_ph():
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
    make_minister(pid)
    set_current_minister(match_id, 0)
    pid2 =add_user_in_match(uid2, match_id, 1).PlayerId
    bid = get_match_board_id(match_id)
    create_deck(bid)
    shuffle_deck(bid)
    get_top_three_proclamation(bid)

    make_director(pid2)
    set_current_director(match_id,1)

    change_ingame_status(match_id, DIRECTOR_SELECTION)

    for i in range (0,4):
        enact_proclamation(match_id,PHOENIX_STR)

    change_selected_deck_phoenix(bid)
    hand_db = show_selected_deck(bid)
    discarted_db = hand_db[0]
    selected_db_1=hand_db[1]
    selected_db_2=hand_db[2]
    discard_proclamation(bid, selected_db_2)
    assert get_failed_election_count(bid)==0
    add_failed_election(bid)
    add_failed_election(bid)
    assert get_failed_election_count(bid)==2

    response = client.post(
        f"/game/{match_id}/proclamation/{pid2}?discarded={discarted_db}",
        json=[selected_db_1]
    )
    assert get_failed_election_count(bid)==0
    assert response.status_code == 200
    assert response.json() == PHOENIX_STR

def test_receive_cards_director_spell():
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
    make_minister(pid)
    set_current_minister(match_id, 0)
    pid2 =add_user_in_match(uid2, match_id, 1).PlayerId
    bid = get_match_board_id(match_id)
    create_deck(bid)
    shuffle_deck(bid)
    get_top_three_proclamation(bid)

    make_director(pid2)
    set_current_director(match_id,1)

    change_ingame_status(match_id, DIRECTOR_SELECTION)

    for i in range (0,2):
        enact_proclamation(match_id,DEATH_EATER_STR)

    change_selected_deck_death_eater(bid)
    hand_db = show_selected_deck(bid)
    discarted_db = hand_db[0]
    selected_db_1 = hand_db[1]
    selected_db_2 = hand_db[2]
    discard_proclamation(bid, selected_db_2)
    assert get_failed_election_count(bid)==0
    add_failed_election(bid)
    assert get_failed_election_count(bid)==1

    response = client.post(
        f"/game/{match_id}/proclamation/{pid2}?discarded={discarted_db}",
        json=[selected_db_1]
    )
    assert get_failed_election_count(bid)==0
    assert response.status_code == 200
    assert response.json() == NO_WINNER_YET
    assert get_ingame_status(match_id) == ingame_status[USE_SPELL]
    assert get_board_status(bid)['spell'] == spells[ADIVINATION]

def test_unlock_expelliarmus():
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
    make_minister(pid)
    set_current_minister(match_id, 0)
    pid2 =add_user_in_match(uid2, match_id, 1).PlayerId
    bid = get_match_board_id(match_id)
    create_deck(bid)
    shuffle_deck(bid)
    get_top_three_proclamation(bid)

    make_director(pid2)
    set_current_director(match_id,1)

    change_ingame_status(match_id, DIRECTOR_SELECTION)

    for i in range(4):
        enact_proclamation(match_id,DEATH_EATER_STR)

    change_selected_deck_death_eater(bid)
    hand_db = show_selected_deck(bid)
    discarted_db = hand_db[0]
    selected_db_1 = hand_db[1]
    selected_db_2 = hand_db[2]
    discard_proclamation(bid, selected_db_2)
    assert get_failed_election_count(bid)==0
    add_failed_election(bid)
    assert get_failed_election_count(bid)==1

    response = client.post(
        f"/game/{match_id}/proclamation/{pid2}?discarded={discarted_db}",
        json=[selected_db_1]
    )
    assert get_failed_election_count(bid)==0
    assert response.status_code == 200
    assert response.json() == NO_WINNER_YET
    assert get_ingame_status(match_id) == ingame_status[USE_SPELL]
    assert get_board_status(bid)['spell'] == spells[AVADA_KEDAVRA]
    assert get_board_status(bid)['expelliarmus'] == expelliarmus[UNLOCKED]

def test_receive_cards_director_fail_ingame():
    delete_data(Board)
    delete_data(Player)
    delete_data(Match)
    delete_data(User)

    create_user("foo1@gmail.com", "bar1", "bar1")
    create_user("bar2@gmail.com", "bar2", "bar2")
    create_user("faa3@gmail.com", "bar3", "bar3")
    create_user("bar4@gmail.com", "bar4", "bar4")
    create_user("foo5@gmail.com", "bar5", "bar5")
    uid1 = get_user("bar1", "bar1")["Id"]
    uid2 = get_user("bar2", "bar2")["Id"]
    uid3 = get_user("bar3", "bar3")["Id"]
    uid4 = get_user("bar4", "bar4")["Id"]
    uid5 = get_user("bar5", "bar5")["Id"]

    match = add_match_db(5,7,uid1)
    match_id = match['Match_id']
    pid = match['Player_id']
    pid2 =add_user_in_match(uid2, match_id, 1).PlayerId
    pid3 =add_user_in_match(uid3, match_id, 3).PlayerId
    pid4 =add_user_in_match(uid4, match_id, 4).PlayerId
    pid5 =add_user_in_match(uid5, match_id, 5).PlayerId

    bid = get_match_board_id(match_id)
    create_deck(bid)
    shuffle_deck(bid)
    get_top_three_proclamation(bid)

    make_minister(pid)
    set_current_minister(match_id, 0)
    make_director(pid3)
    set_current_director(match_id,2)

    change_ingame_status(match_id, MINISTER_SELECTION)

    hand_db = show_selected_deck(bid)
    discarted_db = hand_db[0]
    selected_db_1=hand_db[1]
    selected_db_2=hand_db[2]

    discard_proclamation(bid, selected_db_2)
    assert get_minister_username(match_id)=="bar1"
    assert get_director_username(match_id)=="bar3"

    response = client.post(
        f"/game/{match_id}/proclamation/{pid3}?discarded={discarted_db}",
        json=[selected_db_1]
    )
    assert response.status_code == 404
    assert response.json()['detail'] == "We are not in the director selection stage."

def test_receive_cards_director_fail2():
    delete_data(Board)
    delete_data(Player)
    delete_data(Match)
    delete_data(User)

    create_user("foo1@gmail.com", "bar1", "bar1")
    create_user("bar2@gmail.com", "bar2", "bar2")
    create_user("faa3@gmail.com", "bar3", "bar3")
    create_user("bar4@gmail.com", "bar4", "bar4")
    create_user("foo5@gmail.com", "bar5", "bar5")
    uid1 = get_user("bar1", "bar1")["Id"]
    uid2 = get_user("bar2", "bar2")["Id"]
    uid3 = get_user("bar3", "bar3")["Id"]
    uid4 = get_user("bar4", "bar4")["Id"]
    uid5 = get_user("bar5", "bar5")["Id"]

    match = add_match_db(5,7,uid1)
    match_id = match['Match_id']
    pid = match['Player_id']
    pid2 =add_user_in_match(uid2, match_id, 1).PlayerId
    pid3 =add_user_in_match(uid3, match_id, 3).PlayerId
    pid4 =add_user_in_match(uid4, match_id, 4).PlayerId
    pid5 =add_user_in_match(uid5, match_id, 5).PlayerId

    bid = get_match_board_id(match_id)
    create_deck(bid)
    shuffle_deck(bid)
    get_top_three_proclamation(bid)

    make_minister(pid)
    set_current_minister(match_id, 0)
    make_director(pid3)
    set_current_director(match_id,2)

    change_ingame_status(match_id, DIRECTOR_SELECTION)

    hand_db = show_selected_deck(bid)
    discarted_db = hand_db[0]
    selected_db_1=hand_db[1]
    selected_db_2=hand_db[2]

    assert get_minister_username(match_id)=="bar1"
    assert get_director_username(match_id)=="bar3"

    response = client.post(
        f"/game/{match_id}/proclamation/{pid3}?discarded={discarted_db}",
        json=[selected_db_1, selected_db_2]
    )
    assert response.status_code == 404
    assert response.json()['detail'] == "The number of proclamation selected doesn't match the number of proclamations expected from director."


def test_receive_cards_director_fail3():
    delete_data(Board)
    delete_data(Player)
    delete_data(Match)
    delete_data(User)

    create_user("foo1@gmail.com", "bar1", "bar1")
    create_user("bar2@gmail.com", "bar2", "bar2")
    create_user("faa3@gmail.com", "bar3", "bar3")
    create_user("bar4@gmail.com", "bar4", "bar4")
    create_user("foo5@gmail.com", "bar5", "bar5")
    uid1 = get_user("bar1", "bar1")["Id"]
    uid2 = get_user("bar2", "bar2")["Id"]
    uid3 = get_user("bar3", "bar3")["Id"]
    uid4 = get_user("bar4", "bar4")["Id"]
    uid5 = get_user("bar5", "bar5")["Id"]

    match = add_match_db(5,7,uid1)
    match_id = match['Match_id']
    pid = match['Player_id']
    pid2 =add_user_in_match(uid2, match_id, 1).PlayerId
    pid3 =add_user_in_match(uid3, match_id, 3).PlayerId
    pid4 =add_user_in_match(uid4, match_id, 4).PlayerId
    pid5 =add_user_in_match(uid5, match_id, 5).PlayerId

    bid = get_match_board_id(match_id)
    create_deck(bid)
    shuffle_deck(bid)
    get_top_three_proclamation(bid)

    make_minister(pid)
    set_current_minister(match_id, 0)
    make_director(pid3)
    set_current_director(match_id,2)

    change_ingame_status(match_id, DIRECTOR_SELECTION)

    hand_db = show_selected_deck(bid)
    discarted_db = hand_db[0]
    selected_db_1=hand_db[1]
    selected_db_2=hand_db[2]

    discard_proclamation(bid, selected_db_2)
    assert get_minister_username(match_id)=="bar1"
    assert get_director_username(match_id)=="bar3"

    if selected_db_1 == PHOENIX_STR:
        selected_db_1 = DEATH_EATER_STR
    else:
        selected_db_1=PHOENIX_STR

    response = client.post(
        f"/game/{match_id}/proclamation/{pid3}?discarded={discarted_db}",
        json=[selected_db_1]
    )
    assert response.status_code == 404
    assert response.json()['detail'] == "The proclamation selected doesn't match the proclamations passed."


def test_receive_cards_director_fail_discarded():
    delete_data(Board)
    delete_data(Player)
    delete_data(Match)
    delete_data(User)

    create_user("foo1@gmail.com", "bar1", "bar1")
    create_user("bar2@gmail.com", "bar2", "bar2")
    create_user("faa3@gmail.com", "bar3", "bar3")
    create_user("bar4@gmail.com", "bar4", "bar4")
    create_user("foo5@gmail.com", "bar5", "bar5")
    uid1 = get_user("bar1", "bar1")["Id"]
    uid2 = get_user("bar2", "bar2")["Id"]
    uid3 = get_user("bar3", "bar3")["Id"]
    uid4 = get_user("bar4", "bar4")["Id"]
    uid5 = get_user("bar5", "bar5")["Id"]

    match = add_match_db(5,7,uid1)
    match_id = match['Match_id']
    pid = match['Player_id']
    pid2 =add_user_in_match(uid2, match_id, 1).PlayerId
    pid3 =add_user_in_match(uid3, match_id, 3).PlayerId
    pid4 =add_user_in_match(uid4, match_id, 4).PlayerId
    pid5 =add_user_in_match(uid5, match_id, 5).PlayerId

    bid = get_match_board_id(match_id)
    create_deck(bid)
    shuffle_deck(bid)
    get_top_three_proclamation(bid)

    make_minister(pid)
    set_current_minister(match_id, 0)
    make_director(pid3)
    set_current_director(match_id,2)

    change_ingame_status(match_id, DIRECTOR_SELECTION)

    hand_db = show_selected_deck(bid)
    discarted_db = hand_db[0]
    selected_db_1=hand_db[1]
    selected_db_2=hand_db[2]

    discard_proclamation(bid, selected_db_2)
    assert get_minister_username(match_id)=="bar1"
    assert get_director_username(match_id)=="bar3"

    response = client.post(
        f"/game/{match_id}/proclamation/{pid3}?discarded=descartada",
        json=[selected_db_1]
    )
    assert response.status_code == 404
    assert response.json()['detail'] == "The proclamation discarded doesn't match the proclamations passed."


def test_receive_cards_director_fail_empty_selected():
    delete_data(Board)
    delete_data(Player)
    delete_data(Match)
    delete_data(User)

    create_user("foo1@gmail.com", "bar1", "bar1")
    create_user("bar2@gmail.com", "bar2", "bar2")
    create_user("faa3@gmail.com", "bar3", "bar3")
    create_user("bar4@gmail.com", "bar4", "bar4")
    create_user("foo5@gmail.com", "bar5", "bar5")
    uid1 = get_user("bar1", "bar1")["Id"]
    uid2 = get_user("bar2", "bar2")["Id"]
    uid3 = get_user("bar3", "bar3")["Id"]
    uid4 = get_user("bar4", "bar4")["Id"]
    uid5 = get_user("bar5", "bar5")["Id"]

    match = add_match_db(5,7,uid1)
    match_id = match['Match_id']
    pid = match['Player_id']
    pid2 =add_user_in_match(uid2, match_id, 1).PlayerId
    pid3 =add_user_in_match(uid3, match_id, 3).PlayerId
    pid4 =add_user_in_match(uid4, match_id, 4).PlayerId
    pid5 =add_user_in_match(uid5, match_id, 5).PlayerId

    bid = get_match_board_id(match_id)
    create_deck(bid)
    shuffle_deck(bid)

    make_minister(pid)
    set_current_minister(match_id, 0)
    make_director(pid3)
    set_current_director(match_id,2)

    change_ingame_status(match_id, DIRECTOR_SELECTION)


    assert get_minister_username(match_id)=="bar1"
    assert get_director_username(match_id)=="bar3"

    response = client.post(
        f"/game/{match_id}/proclamation/{pid3}?discarded=phoenix",
        json=[PHOENIX_STR]
    )
    assert response.status_code == 404
    assert response.json()['detail'] == "The proclamation discarded doesn't match the proclamations passed."


def test_receive_cards_director_needed_shufle():
    delete_data(Board)
    delete_data(Player)
    delete_data(Match)
    delete_data(User)

    create_user("foo1@gmail.com", "bar1", "bar1")
    create_user("bar2@gmail.com", "bar2", "bar2")
    create_user("faa3@gmail.com", "bar3", "bar3")
    create_user("bar4@gmail.com", "bar4", "bar4")
    create_user("foo5@gmail.com", "bar5", "bar5")
    uid1 = get_user("bar1", "bar1")["Id"]
    uid2 = get_user("bar2", "bar2")["Id"]
    uid3 = get_user("bar3", "bar3")["Id"]
    uid4 = get_user("bar4", "bar4")["Id"]
    uid5 = get_user("bar5", "bar5")["Id"]

    match = add_match_db(5,7,uid1)
    match_id = match['Match_id']
    pid = match['Player_id']
    pid2 =add_user_in_match(uid2, match_id, 1).PlayerId
    pid3 =add_user_in_match(uid3, match_id, 3).PlayerId
    pid4 =add_user_in_match(uid4, match_id, 4).PlayerId
    pid5 =add_user_in_match(uid5, match_id, 5).PlayerId

    bid = get_match_board_id(match_id)
    create_deck(bid)
    shuffle_deck(bid)

    make_minister(pid)
    set_current_minister(match_id, 0)
    make_director(pid3)
    set_current_director(match_id,2)

    change_ingame_status(match_id, DIRECTOR_SELECTION)

    for i in range(0,4):
        get_top_three_proclamation(bid)
        hand_db = show_selected_deck(bid)
        discarted_db = hand_db[0]
        selected_db_1=hand_db[1]
        selected_db_2=hand_db[2]
        discard_proclamation(bid, selected_db_2)
        discard_proclamation(bid, selected_db_1)
        discard_proclamation(bid, discarted_db)
    
    get_top_three_proclamation(bid)
    hand_db = show_selected_deck(bid)
    discarted_db = hand_db[0]
    selected_db_1=hand_db[1]
    selected_db_2=hand_db[2]
    discard_proclamation(bid, selected_db_2)

    assert get_minister_username(match_id)=="bar1"
    assert get_director_username(match_id)=="bar3"

    response = client.post(
        f"/game/{match_id}/proclamation/{pid3}?discarded={discarted_db}",
        json=[selected_db_1]
    )
    assert response.status_code == 200
    assert response.json() == "no winner yet"
    assert get_ingame_status(match_id) == ingame_status[NOMINATION]
    if selected_db_1 == PHOENIX_STR:
        assert get_phoenix_proclamations(match_id) == 1
        assert get_death_eater_proclamations(match_id) == 0
    else:
        assert get_phoenix_proclamations(match_id) == 0
        assert get_death_eater_proclamations(match_id) == 1
    assert get_minister_username(match_id)=="bar2"
    assert len(show_selected_deck(bid))==3


def test_receive_cards_director_fail_not_dir_or_min():
    delete_data(Board)
    delete_data(Player)
    delete_data(Match)
    delete_data(User)

    create_user("foo1@gmail.com", "bar1", "bar1")
    create_user("bar2@gmail.com", "bar2", "bar2")
    create_user("faa3@gmail.com", "bar3", "bar3")
    create_user("bar4@gmail.com", "bar4", "bar4")
    create_user("foo5@gmail.com", "bar5", "bar5")
    uid1 = get_user("bar1", "bar1")["Id"]
    uid2 = get_user("bar2", "bar2")["Id"]
    uid3 = get_user("bar3", "bar3")["Id"]
    uid4 = get_user("bar4", "bar4")["Id"]
    uid5 = get_user("bar5", "bar5")["Id"]

    match = add_match_db(5,7,uid1)
    match_id = match['Match_id']
    pid = match['Player_id']
    pid2 =add_user_in_match(uid2, match_id, 1).PlayerId
    pid3 =add_user_in_match(uid3, match_id, 3).PlayerId
    pid4 =add_user_in_match(uid4, match_id, 4).PlayerId
    pid5 =add_user_in_match(uid5, match_id, 5).PlayerId

    bid = get_match_board_id(match_id)
    create_deck(bid)
    shuffle_deck(bid)
    get_top_three_proclamation(bid)

    make_minister(pid)
    set_current_minister(match_id, 0)
    make_director(pid3)
    set_current_director(match_id,2)

    change_ingame_status(match_id, DIRECTOR_SELECTION)

    hand_db = show_selected_deck(bid)
    discarted_db = hand_db[0]
    selected_db_1=hand_db[1]
    selected_db_2=hand_db[2]

    discard_proclamation(bid, selected_db_2)
    assert get_minister_username(match_id)=="bar1"
    assert get_director_username(match_id)=="bar3"

    response = client.post(
        f"/game/{match_id}/proclamation/{pid5}?discarded={discarted_db}",
        json=[selected_db_1]
    )
    assert response.status_code == 404
    assert response.json()['detail'] == "This user is not the director or the minister."
