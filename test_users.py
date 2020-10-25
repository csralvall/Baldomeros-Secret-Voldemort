from fastapi.testclient import TestClient

from crud import delete_user

from users import app

client = TestClient(app)

def test_register_user_empty_email():

    response = client.post(
        "/account",
        data={
            "email": "",
            "username": "foo",
            "password": "foo"}
    )

    assert response.status_code == 422
    assert response.json()['detail'][0]['msg'] == "field required"

def test_register_user_empty_username():

    response = client.post(
        "/account",
        data={
            "email": "foo@foo.com",
            "username": "",
            "password": "foo"}
    )

    assert response.status_code == 422
    assert response.json()['detail'][0]['msg'] == "field required"

def test_register_user_empty_password():

    response = client.post(
        "/account",
        data={
            "email": "foo@foo.com",
            "username": "foo",
            "password": ""}
    )

    assert response.status_code == 422
    assert response.json()['detail'][0]['msg'] == "field required"

def test_register_user_bad_email():
    response = client.post(
        "/account",
        data={
            "email": "foo@foo@foo.com",
            "username": "foo",
            "password": "foo"}
    )

    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {"loc": ["body","email"],
            "msg": "value is not a valid email address",
            "type": "value_error.email"}]
        }

def test_register_user_used_email():

    client.post(
        "/account",
        data={
            "email": "baz@gmail.com",
            "username": "baz",
            "password": "baz"})

    response = client.post(
        "/account",
        data={
            "email": "baz@gmail.com",
            "username": "foo",
            "password": "foo"}
    )

    delete_user("baz@gmail.com","baz","baz")

    assert response.status_code == 409
    assert response.json() == {"detail": "Email already registered"}

def test_register_user_used_username():

    client.post(
        "/account",
        data={
            "email": "baz@gmail.com",
            "username": "baz",
            "password": "baz"}
    )

    response = client.post(
        "/account",
        data={
            "email": "rem@gmail.com",
            "username": "baz",
            "password": "foo"}
    )

    delete_user("baz@gmail.com","baz","baz")

    assert response.status_code == 409
    assert response.json() == {"detail": "Username already taken"}

def test_register_user_correct():

    delete_user("foo@gmail.com","foo","foo")

    response = client.post(
        "/account",
        data={
            "email": "foo@gmail.com",
            "username": "foo",
            "password": "foo"}
    )

    assert response.status_code == 201
    assert response.json() == {
        "email": "foo@gmail.com",
        "username": "foo"}
