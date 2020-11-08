from fastapi.testclient import TestClient

from server.db.crud import *

from server.main import app

client = TestClient(app)

def test_start_game_5():
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
    create_user("one3@gmail.com","one3","one")
    aux3 = get_user("one3", "one")
    auxid3 = aux3["Id"] 
    create_user("one4@gmail.com","one4","one")
    aux4 = get_user("one4", "one")
    auxid4 = aux4["Id"] 
    create_user("one5@gmail.com","one5","one")
    aux5 = get_user("one5", "one")
    auxid5 = aux5["Id"]     

    add_user_in_match(auxid2, gidauxid, 1)
    add_user_in_match(auxid3, gidauxid, 1)
    add_user_in_match(auxid4, gidauxid, 1)
    add_user_in_match(auxid5, gidauxid, 1)


    response = client.patch(
        f"/game/{gidauxid}?user={auxid}"
    )

    assert response.status_code == 200
