from fastapi.testclient import TestClient

from server.tests.helpers import *
from server.db.crud import *

from server.main import app

client = TestClient(app)

def test_match_not_exist():
    delete_data(Board)
    delete_data(Player)
    delete_data(Match)
    delete_data(User)

    mid = 1

    response = client.get(
        f"game/{mid}/directors"
    )

    assert response.status_code == 404

def test__match_exist():
    delete_data(Board)
    delete_data(Player)
    delete_data(Match)
    delete_data(User)

    create_user("foo@gmail.com", "foo", "foo")
    user = get_user("foo", "foo")
    uid = user['Id']

    mid = add_match_db(5,7,uid)['Match_id']

    response = client.get(
        f"game/{mid}/directors"
    )

    assert response.status_code == 200

def test_get_directors_5_players():
    delete_data(Board)
    delete_data(Player)
    delete_data(Match)
    delete_data(User)

    create_user("example2@gmail.com","example2", "password")
    create_user("example3@gmail.com","example3","password")
    create_user("example4@gmail.com","example4","password")
    create_user("example5@gmail.com","example5","password")
    create_user("example6@gmail.com","example6","password")

    user = get_user("example2", "password")
    uid = user['Id']
    match = add_match_db(5,7,uid)
    mid = match['Match_id']

    user2 = get_user("example3", "password")
    user2id = user2['Id']
    user3 = get_user("example4", "password")
    user3id = user3['Id']
    user4 = get_user("example5", "password")
    user4id = user4['Id']
    user5 = get_user("example6", "password")
    user5id = user5['Id']

    player2 = add_user_in_match(user2id,mid,2)
    player3 = add_user_in_match(user3id,mid,3)
    player4 = add_user_in_match(user4id,mid,4)
    player5 = add_user_in_match(user5id,mid,5)

    player1id = match["Player_id"]
    player2id = player2.to_dict("PlayerId")["PlayerId"]
    player3id = player3.to_dict("PlayerId")["PlayerId"]
    player4id = player4.to_dict("PlayerId")["PlayerId"]
    player5id = player5.to_dict("PlayerId")["PlayerId"]

    change_player_rol(player2id,0) #voldemort
    change_player_rol(player3id,1) #death_eater
    change_player_rol(player4id,2) #phoenix
    change_player_rol(player5id,2) #phoenix

    make_magician(player1id)
    make_magician(player2id)
    make_magician(player3id)
    make_magician(player4id)
    make_magician(player5id)

    make_minister(player5id)

    change_last_director(mid,2) #example3
    change_last_director_govrol(player2id)#example3
    kill_player(player3id) #example4
    make_ex_minister(player4id)#example5

    response = client.get(
        f"game/{mid}/directors"
    )

    assert response.status_code == 200
    assert response.json() == {"posible directors": ['example2','example5']}



def test_get_directors_7_players():
    delete_data(Board)
    delete_data(Player)
    delete_data(Match)
    delete_data(User)

    create_user("example1@gmail.com","example1", "password")
    create_user("example2@gmail.com","example2", "password")
    create_user("example3@gmail.com","example3","password")
    create_user("example4@gmail.com","example4","password")
    create_user("example5@gmail.com","example5","password")
    create_user("example6@gmail.com","example6","password")
    create_user("example7@gmail.com","example7", "password")

    user1 = get_user("example1", "password")
    user1id = user1['Id']
    match = add_match_db(5,7,user1id)
    mid = match['Match_id']

    user2 = get_user("example2", "password")
    user2id = user2['Id']
    user3 = get_user("example3", "password")
    user3id = user3['Id']
    user4 = get_user("example4", "password")
    user4id = user4['Id']
    user5 = get_user("example5", "password")
    user5id = user5['Id']
    user6 = get_user("example6", "password")
    user6id = user6['Id']
    user7 = get_user("example7", "password")
    user7id = user7['Id']

    player2 = add_user_in_match(user2id,mid,2)
    player3 = add_user_in_match(user3id,mid,3)
    player4 = add_user_in_match(user4id,mid,4)
    player5 = add_user_in_match(user5id,mid,5)
    player6 = add_user_in_match(user6id,mid,6)
    player7 = add_user_in_match(user7id,mid,7)

    player1id = match["Player_id"]
    player2id = player2.to_dict("PlayerId")["PlayerId"]
    player3id = player3.to_dict("PlayerId")["PlayerId"]
    player4id = player4.to_dict("PlayerId")["PlayerId"]
    player5id = player5.to_dict("PlayerId")["PlayerId"]
    player6id = player6.to_dict("PlayerId")["PlayerId"]
    player7id = player7.to_dict("PlayerId")["PlayerId"]

    change_player_rol(player2id,0) #voldemort
    change_player_rol(player3id,1) #death_eater
    change_player_rol(player4id,2) #phoenix
    change_player_rol(player5id,2) #phoenix
    change_player_rol(player6id,1) #death_eater
    change_player_rol(player7id,2) #phoenix

    make_magician(player1id)
    make_magician(player2id)
    make_magician(player3id)
    make_magician(player4id)
    make_magician(player5id)
    make_magician(player6id)
    make_magician(player7id)

    make_minister(player5id)#example 5 es ministro
    change_last_director_govrol(player2id)#example2 es exdirector
    make_ex_minister(player4id)#example4 es exministro

    response = client.get(
        f"game/{mid}/directors"
    )

    assert response.status_code == 200
    assert response.json() == {"posible directors": ['example1','example3','example6','example7']}

    kill_player(player1id)
    kill_player(player3id)
    #example1 y example 3 estan muertos, no tienen que salir
    #example 5 es ministro
    #example2 es exdirector
    #example4 es exministro, esta vez si deberia estar, porque son 5 jugadores vivos

    response2 = client.get(
        f"game/{mid}/directors"
    )

    assert response2.status_code == 200
    assert response2.json() == {"posible directors": ['example4','example6','example7']}
