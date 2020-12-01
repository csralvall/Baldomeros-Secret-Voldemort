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


from server.db.dicts import *

from server.tests.helpers import *

from server.main import app

client = TestClient(app)


def test_chat_ok():
    delete_data(Board)
    delete_data(Player)
    delete_data(Match)
    delete_data(User)

    create_user("rt@gmail.com", "rteee", "rteee")
    user1 = get_user("rteee", "rteee")
    user1id = user1["Id"] 
    username = "rteee"

    match = add_match_db("5", "5", user1id)
    match_id = match["Match_id"]
    
    message = "hola a todos"

    response = client.patch(
        f"/game/{match_id}/chat?username={username}",
        json= message
    )
    assert response.status_code == 200
    assert response.json() == "Message sent"
    assert read_messages(match_id) == {0:{"Username":username,"Text":message}}


    create_user("user2@gmail.com", "user2", "user2")
    user2 = get_user("user2", "user2")
    user2id = user2["Id"] 
    username2 = "user2"
    add_user_in_match(user2id,match_id,1)
    message2 = "chau"

    response2 = client.patch(
        f"/game/{match_id}/chat?username={username2}",
        json= message2
    )
    assert response.status_code == 200
    assert response.json() == "Message sent"
    assert read_messages(match_id) == {0:{"Username":username,"Text":message},1:{"Username":username2,"Text":message2}}


def test_chat_wrong_match_id():
    delete_data(Board)
    delete_data(Player)
    delete_data(Match)
    delete_data(User)

    create_user("rt@gmail.com", "rteee", "rteee")
    user1 = get_user("rteee", "rteee")
    user1id = user1["Id"] 
    username = "rteee"

    match = add_match_db("5", "5", user1id)
    match_id = match["Match_id"]
    
    message = "hola a todos"

    response = client.patch(
        f"/game/{match_id+1}/chat?username={username}",
        json= message
    )
    assert response.status_code == 404
    assert response.json()['detail'] == "Match not found"
    assert read_messages(match_id) == {}

def test_chat_wrong_username():
    delete_data(Board)
    delete_data(Player)
    delete_data(Match)
    delete_data(User)

    create_user("rt@gmail.com", "rteee", "rteee")
    user1 = get_user("rteee", "rteee")
    user1id = user1["Id"] 
    username = "rteee2"

    match = add_match_db("5", "5", user1id)
    match_id = match["Match_id"]
    
    message = "hola a todos"

    response = client.patch(
        f"/game/{match_id}/chat?username={username}",
        json= message
    )
    assert response.status_code == 404
    assert response.json()['detail'] == "This user is not playing this match"
    assert read_messages(match_id) == {}


def test_chat_player_dead():
    delete_data(Board)
    delete_data(Player)
    delete_data(Match)
    delete_data(User)

    create_user("rt@gmail.com", "rteee", "rteee")
    user1 = get_user("rteee", "rteee")
    user1id = user1["Id"] 
    username = "rteee"
    create_user("user2@gmail.com", "user2", "user2")
    user2 = get_user("user2", "user2")
    user2id = user2["Id"] 
    username2 = "user2"

    match = add_match_db("5", "5", user1id)
    match_id = match["Match_id"]
    player2_id = add_user_in_match(user2id,match_id,1).PlayerId
    message = "chau"

    kill_player(player2_id)

    response = client.patch(
        f"/game/{match_id}/chat?username={username2 }",
        json= message
    )
    assert response.status_code == 404
    assert response.json()['detail'] == "Player is dead"
    assert read_messages(match_id) == {}
    
def test_chat_minister_bad1():
    delete_data(Board)
    delete_data(Player)
    delete_data(Match)
    delete_data(User)

    create_user("rt@gmail.com", "rteee", "rteee")
    user1 = get_user("rteee", "rteee")
    user1id = user1["Id"] 
    username = "rteee"
    create_user("user2@gmail.com", "user2", "user2")
    user2 = get_user("user2", "user2")
    user2id = user2["Id"] 
    username2 = "user2"

    match = add_match_db("5", "5", user1id)
    match_id = match["Match_id"]
    player_id = match["Player_id"]
    player2_id = add_user_in_match(user2id,match_id,1).PlayerId
    message = "chau"
    make_magician(player_id)
    make_minister(player2_id)
    set_current_minister(match_id, 1)
    change_ingame_status(match_id, MINISTER_SELECTION)
    assert(get_ingame_status(match_id)==MINISTER_SELECTION)
    assert(get_minister_username(match_id)==username2)

    response = client.patch(
        f"/game/{match_id}/chat?username={username2 }",
        json= message
    )
    assert response.status_code == 404
    assert response.json()['detail'] == "Minister and director can't talk during legislative session"
    assert read_messages(match_id) == {}
    change_ingame_status(match_id, DIRECTOR_SELECTION)
    assert(get_ingame_status(match_id)==DIRECTOR_SELECTION)
    assert(get_minister_username(match_id)==username2)

    response = client.patch(
        f"/game/{match_id}/chat?username={username2 }",
        json= message
    )
    assert response.status_code == 404
    assert response.json()['detail'] == "Minister and director can't talk during legislative session"
    assert read_messages(match_id) == {}

    change_ingame_status(match_id, USE_SPELL)
    assert(get_ingame_status(match_id)==USE_SPELL)
    assert(get_minister_username(match_id)==username2)
    response = client.patch(
        f"/game/{match_id}/chat?username={username2 }",
        json= message
    )
    assert response.status_code == 200
    assert response.json() == "Message sent"
    assert read_messages(match_id) == {0:{"Username":username2,"Text":message}}

def test_chat_director_bad():
    delete_data(Board)
    delete_data(Player)
    delete_data(Match)
    delete_data(User)

    create_user("rt@gmail.com", "rteee", "rteee")
    user1 = get_user("rteee", "rteee")
    user1id = user1["Id"] 
    username = "rteee"
    create_user("user2@gmail.com", "user2", "user2")
    user2 = get_user("user2", "user2")
    user2id = user2["Id"] 
    username2 = "user2"

    match = add_match_db("5", "5", user1id)
    match_id = match["Match_id"]
    player_id = match["Player_id"]
    player2_id = add_user_in_match(user2id,match_id,1).PlayerId
    message = "chau"
    make_magician(player_id)
    make_director(player2_id)
    set_current_director(match_id, 1)
    change_ingame_status(match_id, MINISTER_SELECTION)
    assert(get_ingame_status(match_id)==MINISTER_SELECTION)
    assert(get_director_username(match_id)==username2)

    response = client.patch(
        f"/game/{match_id}/chat?username={username2 }",
        json= message
    )
    assert response.status_code == 404
    assert response.json()['detail'] == "Minister and director can't talk during legislative session"
    assert read_messages(match_id) == {}
    change_ingame_status(match_id, DIRECTOR_SELECTION)
    assert(get_ingame_status(match_id)==DIRECTOR_SELECTION)
    assert(get_director_username(match_id)==username2)

    response = client.patch(
        f"/game/{match_id}/chat?username={username2 }",
        json= message
    )
    assert response.status_code == 404
    assert response.json()['detail'] == "Minister and director can't talk during legislative session"
    assert read_messages(match_id) == {}

    change_ingame_status(match_id, USE_SPELL)
    assert(get_ingame_status(match_id)==USE_SPELL)
    assert(get_director_username(match_id)==username2)
    response = client.patch(
        f"/game/{match_id}/chat?username={username2 }",
        json= message
    )
    assert response.status_code == 200
    assert response.json() == "Message sent"
    assert read_messages(match_id) == {0:{"Username":username2,"Text":message}}

