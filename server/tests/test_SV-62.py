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
    aux = get_user("one", "one")
    auxid = aux["Id"] 

    gidaux = add_match_db(5, 5, auxid)
    gidauxid = gidaux["Match_id"]

    create_user("one2@gmail.com","one2","one")
    aux2 = get_user("one2", "one")
    auxid2 = aux2["Id"]     

    gidaux2 = add_match_db(7, 10, auxid2)
    gidauxid2 = gidaux2["Match_id"]

    create_user("one3@gmail.com","one3","one")
    aux3 = get_user("one3", "one")
    auxid3 = aux3["Id"] 
 
    gidaux3 = add_match_db(6, 8, auxid3)
    gidauxid3 = gidaux3["Match_id"]

    response = client.get(
        "/game/list"
    )

    assert response.status_code == 200
