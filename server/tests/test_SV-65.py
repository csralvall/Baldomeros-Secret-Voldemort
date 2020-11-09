from fastapi.testclient import TestClient

from server.db.crud import *

from server.main import app

from server.tests.helpers import *

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
    add_user_in_match(auxid3, gidauxid, 2)
    add_user_in_match(auxid4, gidauxid, 3)
    add_user_in_match(auxid5, gidauxid, 4)

    response = client.patch(
        f"/game/{gidauxid}?user={auxid}"
    )

    assert response.status_code == 200

def test_start_game_6():
    delete_data(Board)
    delete_data(Player)
    delete_data(Match)
    delete_data(User)

    create_user("one@gmail.com","one","one")
    aux = get_user("one", "one")
    auxid = aux["Id"] 

    gidaux = add_match_db(6, 6, auxid)
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
    create_user("one6@gmail.com","one6","one")
    aux6 = get_user("one6", "one")
    auxid6 = aux6["Id"]              

    add_user_in_match(auxid2, gidauxid, 1)
    add_user_in_match(auxid3, gidauxid, 2)
    add_user_in_match(auxid4, gidauxid, 3)
    add_user_in_match(auxid5, gidauxid, 4)
    add_user_in_match(auxid6, gidauxid, 5)

    response = client.patch(
        f"/game/{gidauxid}?user={auxid}"
    )

    assert response.status_code == 200

def test_start_game_7():
    delete_data(Board)
    delete_data(Player)
    delete_data(Match)
    delete_data(User)

    create_user("one@gmail.com","one","one")
    aux = get_user("one", "one")
    auxid = aux["Id"] 

    gidaux = add_match_db(7, 7, auxid)
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
    create_user("one6@gmail.com","one6","one")
    aux6 = get_user("one6", "one")
    auxid6 = aux6["Id"]   
    create_user("one7@gmail.com","one7","one")
    aux7 = get_user("one7", "one")
    auxid7 = aux7["Id"]                

    add_user_in_match(auxid2, gidauxid, 1)
    add_user_in_match(auxid3, gidauxid, 2)
    add_user_in_match(auxid4, gidauxid, 3)
    add_user_in_match(auxid5, gidauxid, 4)
    add_user_in_match(auxid6, gidauxid, 5)
    add_user_in_match(auxid7, gidauxid, 6)

    response = client.patch(
        f"/game/{gidauxid}?user={auxid}"
    )

    assert response.status_code == 200

def test_start_game_8():
    delete_data(Board)
    delete_data(Player)
    delete_data(Match)
    delete_data(User)

    create_user("one@gmail.com","one","one")
    aux = get_user("one", "one")
    auxid = aux["Id"] 

    gidaux = add_match_db(8, 8, auxid)
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
    create_user("one6@gmail.com","one6","one")
    aux6 = get_user("one6", "one")
    auxid6 = aux6["Id"]   
    create_user("one7@gmail.com","one7","one")
    aux7 = get_user("one7", "one")
    auxid7 = aux7["Id"] 
    create_user("one8@gmail.com","one8","one")
    aux8 = get_user("one8", "one")
    auxid8 = aux8["Id"]                    

    add_user_in_match(auxid2, gidauxid, 1)
    add_user_in_match(auxid3, gidauxid, 2)
    add_user_in_match(auxid4, gidauxid, 3)
    add_user_in_match(auxid5, gidauxid, 4)
    add_user_in_match(auxid6, gidauxid, 5)
    add_user_in_match(auxid7, gidauxid, 6)
    add_user_in_match(auxid8, gidauxid, 7)

    response = client.patch(
        f"/game/{gidauxid}?user={auxid}"
    )

    assert response.status_code == 200    

def test_start_game_9():
    delete_data(Board)
    delete_data(Player)
    delete_data(Match)
    delete_data(User)

    create_user("one@gmail.com","one","one")
    aux = get_user("one", "one")
    auxid = aux["Id"] 

    gidaux = add_match_db(9, 9, auxid)
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
    create_user("one6@gmail.com","one6","one")
    aux6 = get_user("one6", "one")
    auxid6 = aux6["Id"]   
    create_user("one7@gmail.com","one7","one")
    aux7 = get_user("one7", "one")
    auxid7 = aux7["Id"] 
    create_user("one8@gmail.com","one8","one")
    aux8 = get_user("one8", "one")
    auxid8 = aux8["Id"]   
    create_user("one9@gmail.com","one9","one")
    aux9 = get_user("one9", "one")
    auxid9 = aux9["Id"]                      

    add_user_in_match(auxid2, gidauxid, 1)
    add_user_in_match(auxid3, gidauxid, 2)
    add_user_in_match(auxid4, gidauxid, 3)
    add_user_in_match(auxid5, gidauxid, 4)
    add_user_in_match(auxid6, gidauxid, 5)
    add_user_in_match(auxid7, gidauxid, 6)
    add_user_in_match(auxid8, gidauxid, 7)
    add_user_in_match(auxid9, gidauxid, 8)

    response = client.patch(
        f"/game/{gidauxid}?user={auxid}"
    )

    assert response.status_code == 200    

def test_start_game_10():
    delete_data(Board)
    delete_data(Player)
    delete_data(Match)
    delete_data(User)

    create_user("one@gmail.com","one","one")
    aux = get_user("one", "one")
    auxid = aux["Id"] 

    gidaux = add_match_db(10, 10, auxid)
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
    create_user("one6@gmail.com","one6","one")
    aux6 = get_user("one6", "one")
    auxid6 = aux6["Id"]   
    create_user("one7@gmail.com","one7","one")
    aux7 = get_user("one7", "one")
    auxid7 = aux7["Id"] 
    create_user("one8@gmail.com","one8","one")
    aux8 = get_user("one8", "one")
    auxid8 = aux8["Id"]   
    create_user("one9@gmail.com","one9","one")
    aux9 = get_user("one9", "one")
    auxid9 = aux9["Id"] 
    create_user("one10@gmail.com","one10","one")
    aux10 = get_user("one10", "one")
    auxid10 = aux10["Id"]                          

    add_user_in_match(auxid2, gidauxid, 1)
    add_user_in_match(auxid3, gidauxid, 2)
    add_user_in_match(auxid4, gidauxid, 3)
    add_user_in_match(auxid5, gidauxid, 4)
    add_user_in_match(auxid6, gidauxid, 5)
    add_user_in_match(auxid7, gidauxid, 6)
    add_user_in_match(auxid8, gidauxid, 7)
    add_user_in_match(auxid9, gidauxid, 8)
    add_user_in_match(auxid10, gidauxid, 9)

    response = client.patch(
        f"/game/{gidauxid}?user={auxid}"
    )

    assert response.status_code == 200    

def test_start_game_fail_mid():
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

    trash = 666

    response = client.patch(
        f"/game/{trash}?user={auxid}"
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "this game does not exist"}

def test_start_game_user_nothost():
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
        f"/game/{gidauxid}?user={auxid3}"
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "only the host can start the game"} 


def test_start_game_empty_mid():
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
    add_user_in_match(auxid3, gidauxid, 2)
    add_user_in_match(auxid4, gidauxid, 3)
    add_user_in_match(auxid5, gidauxid, 4)

    response = client.patch(
        f"/game/?user={auxid}"
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Not Found"}   

def test_start_game_empty_user():
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
    add_user_in_match(auxid3, gidauxid, 2)
    add_user_in_match(auxid4, gidauxid, 3)
    add_user_in_match(auxid5, gidauxid, 4)

    response = client.patch(
        f"/game/{gidauxid}"
    )

    assert response.status_code == 422
    assert response.json()['detail'][0]['msg'] == "field required"  


def test_start_game_less_people():
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


    add_user_in_match(auxid2, gidauxid, 1)
    add_user_in_match(auxid3, gidauxid, 2)
    add_user_in_match(auxid4, gidauxid, 3)


    response = client.patch(
        f"/game/{gidauxid}?user={auxid}"
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "we need more people to start :)"}                  

