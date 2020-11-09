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

def test_death_eater_in_match():
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
    mid = add_match_db(5,7,uid)['Match_id']

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

    player2id = player2.to_dict("PlayerId")["PlayerId"]
    player3id = player3.to_dict("PlayerId")["PlayerId"]
    player4id = player4.to_dict("PlayerId")["PlayerId"]
    player5id = player5.to_dict("PlayerId")["PlayerId"]

    change_player_rol(player2id,0) #voldemort
    change_player_rol(player3id,1) #death_eater
    change_player_rol(player4id,2) #phoenix
    change_player_rol(player5id,2) #phoenix

    change_last_director(mid,2) #example3
    change_last_director_govrol(player2id)
    kill_player(player3id) 

    response = client.get(
        f"game/{mid}/directors"
    )

    assert response.status_code == 200
    assert response.json() == {"posible directors": ['example2','example5','example6']}