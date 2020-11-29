from fastapi.testclient import TestClient

from server.db.crud import *

from server.db.dicts import *

from server.main import app

from server.tests.helpers import *

client = TestClient(app)

def test_give_user_data_ok():
    delete_data(Board)
    delete_data(Player)
    delete_data(Match)
    delete_data(User)

    create_user("one@gmail.com","one","old")
    aux = get_user("one", "old")
    auxid = aux["Id"] 

    response = client.post(
        f"/game/profile?user_id={auxid}"
    )   

    assert response.status_code == 200

def test_give_user_data_bad_userid():
    delete_data(Board)
    delete_data(Player)
    delete_data(Match)
    delete_data(User)

    create_user("one@gmail.com","one","old")
    aux = get_user("one", "old")
    auxid = aux["Id"]

    trash = 666

    response = client.post(
        f"/game/profile?user_id={trash}"
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "failed giving user data"} 

def test_give_user_data_empty_userid():
    delete_data(Board)
    delete_data(Player)
    delete_data(Match)
    delete_data(User)

    create_user("one@gmail.com","one","old")
    aux = get_user("one", "old")
    auxid = aux["Id"]

    trash = 666

    response = client.post(
        f"/game/profile"
    )

    assert response.status_code == 422
    assert response.json()['detail'][0]['msg'] == "field required"  