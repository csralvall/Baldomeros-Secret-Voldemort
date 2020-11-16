from fastapi.testclient import TestClient

from server.db.crud import *

from server.main import app

from server.tests.helpers import *

client = TestClient(app)

def test_adivination_ok():

    delete_data(Board)
    delete_data(Player)
    delete_data(Match)
    delete_data(User)

    create_user("example1@gmail.com","example1", "password")
    user1id = get_user("example1","password")["Id"]

    game1 = add_match_db(5, 5, user1id) 

    create_user("example2@gmail.com","example2", "password")
    user2id = get_user("example2","password")["Id"]
    create_user("example3@gmail.com","example3", "password")
    user3id = get_user("example3","password")["Id"]
    create_user("example4@gmail.com","example4", "password")
    user4id = get_user("example4","password")["Id"]
    create_user("example5@gmail.com","example5", "password")
    user5id = get_user("example5","password")["Id"]

    matchid1 = game1['Match_id']

    add_user_in_match(user2id, matchid1, 1)
    add_user_in_match(user3id, matchid1, 2)
    add_user_in_match(user4id, matchid1, 3)
    add_user_in_match(user5id, matchid1, 4)

    pid1 = get_player_id(matchid1, user1id)
    pid2 = get_player_id(matchid1, user2id)
    pid3 = get_player_id(matchid1, user3id)
    pid4 = get_player_id(matchid1, user4id)
    pid5 = get_player_id(matchid1, user5id)

    make_magician(pid1)
    make_magician(pid2)
    make_magician(pid3)
    make_magician(pid4)
    make_magician(pid5)

    make_minister(pid1)
    make_director(pid2)    

    set_current_minister(matchid1, 0)
    set_current_director(matchid1, 1)

    response = client.patch(
        f"/game/{matchid1}/board/adivination"
    )

    assert response.status_code == 200

def test_adivination_bad_match_id():

    delete_data(Board)
    delete_data(Player)
    delete_data(Match)
    delete_data(User)

    create_user("example1@gmail.com","example1", "password")
    user1id = get_user("example1","password")["Id"]

    game1 = add_match_db(5, 5, user1id) 

    create_user("example2@gmail.com","example2", "password")
    user2id = get_user("example2","password")["Id"]
    create_user("example3@gmail.com","example3", "password")
    user3id = get_user("example3","password")["Id"]
    create_user("example4@gmail.com","example4", "password")
    user4id = get_user("example4","password")["Id"]
    create_user("example5@gmail.com","example5", "password")
    user5id = get_user("example5","password")["Id"]

    matchid1 = game1['Match_id']

    add_user_in_match(user2id, matchid1, 1)
    add_user_in_match(user3id, matchid1, 2)
    add_user_in_match(user4id, matchid1, 3)
    add_user_in_match(user5id, matchid1, 4)

    pid1 = get_player_id(matchid1, user1id)
    pid2 = get_player_id(matchid1, user2id)
    pid3 = get_player_id(matchid1, user3id)
    pid4 = get_player_id(matchid1, user4id)
    pid5 = get_player_id(matchid1, user5id)

    make_magician(pid1)
    make_magician(pid2)
    make_magician(pid3)
    make_magician(pid4)
    make_magician(pid5)

    make_minister(pid1)
    make_director(pid2)    

    set_current_minister(matchid1, 0)
    set_current_director(matchid1, 1)

    trash = 666

    response = client.patch(
        f"/game/{trash}/board/adivination"
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Match not found"} 

