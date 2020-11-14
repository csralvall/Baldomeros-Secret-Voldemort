from fastapi.testclient import TestClient

from server.db.crud import *

from server.main import app

from server.tests.helpers import *

client = TestClient(app)

def test_list_games_ok():
    delete_data(Board)
    delete_data(Player)
    delete_data(Match)
    delete_data(User)

    create_user("one@gmail.com","one","one")
    user = get_user("one", "one")
    user_id = user["Id"] 

    game = add_match_db(5, 5, user_id)
    game_id = game["Match_id"]

    create_user("one2@gmail.com","one2","one")
    user2 = get_user("one2", "one")
    user_id_2 = user2["Id"]     

    game_2 = add_match_db(7, 10, user_id_2)
    game_id_2 = game_2["Match_id"]

    create_user("one3@gmail.com","one3","one")
    user_3 = get_user("one3", "one")
    user_id_3 = user_3["Id"] 
 
    game_3 = add_match_db(6, 8, user_id_3)
    game_id_3 = game_3["Match_id"]

    response = client.get(
        "/game/list"
    )

    assert response.status_code == 200
    assert response.json() == [
        {'Match_id':game_id , 'Min_and_Max': [5, 5], 'Nombre_partida': 'one'},
        {'Match_id':game_id_2 , 'Min_and_Max': [7, 10], 'Nombre_partida': 'one2'},
        {'Match_id':game_id_3 , 'Min_and_Max': [6, 8], 'Nombre_partida': 'one3'} ]

def test_list_games_no_games():
    delete_data(Board)
    delete_data(Player)
    delete_data(Match)
    delete_data(User)

    response = client.get(
        "/game/list"
    )

    assert response.status_code == 200
    assert response.json() == []

