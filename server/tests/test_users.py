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


from server.tests.helpers import *

from server.main import app

client = TestClient(app)

def test_register_user_empty_email():
    delete_data(Board)
    delete_data(Player)
    delete_data(Match)
    delete_data(User)

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
    delete_data(Board)
    delete_data(Player)
    delete_data(Match)
    delete_data(User)

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
    delete_data(Board)
    delete_data(Player)
    delete_data(Match)
    delete_data(User)

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
    delete_data(Board)
    delete_data(Player)
    delete_data(Match)
    delete_data(User)

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
    delete_data(Board)
    delete_data(Player)
    delete_data(Match)
    delete_data(User)

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
    delete_data(Board)
    delete_data(Player)
    delete_data(Match)
    delete_data(User)

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
    delete_data(Board)
    delete_data(Player)
    delete_data(Match)
    delete_data(User)

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

def test_login_user_correct_user():
    delete_data(Board)
    delete_data(Player)
    delete_data(Match)
    delete_data(User)

    response = client.post(
        "/account",
        data={
            "email": "bar@gmail.com",
            "username": "bar",
            "password": "bar"}
    )

    response = client.post(
        "/session",
        data={
            "username": "bar",
            "password": "bar"}
    )

    delete_user("bar@gmail.com","bar","bar")

    assert response.status_code == 200
    assert response.json()['username'] == "bar"

def test_login_user_bad_name():
    delete_data(Board)
    delete_data(Player)
    delete_data(Match)
    delete_data(User)

    response = client.post(
        "/account",
        data={
            "email": "bar@gmail.com",
            "username": "bar",
            "password": "bar"}
    )

    response = client.post(
        "/session",
        data={
            "username": "car",
            "password": "bar"}
    )

    delete_user("bar@gmail.com","bar","bar")

    assert response.status_code == 401
    assert response.json() == {
        "detail": "User not found"
    }

def test_login_user_bad_password():
    delete_data(Board)
    delete_data(Player)
    delete_data(Match)
    delete_data(User)

    response = client.post(
        "/account",
        data={
            "email": "bar@gmail.com",
            "username": "bar",
            "password": "bar",
        },
    )

    response = client.post(
        "/session",
        data={
            "username": "bar",
            "password": "zar"}
    )

    delete_user("bar@gmail.com","bar","bar")

    assert response.status_code == 401
    assert response.json() == {
        "detail": "User not found"
    }

def test_login_user_empty_username():
    delete_data(Board)
    delete_data(Player)
    delete_data(Match)
    delete_data(User)

    response = client.post(
        "/session",
        data={
            "username": "",
            "password": "zar"}
    )

    assert response.status_code == 422
    assert response.json()['detail'][0]['msg'] == "field required"

def test_login_user_empty_password():
    delete_data(Board)
    delete_data(Player)
    delete_data(Match)
    delete_data(User)

    response = client.post(
        "/session",
        data={
            "username": "",
            "password": "zar"}
    )

    assert response.status_code == 422
    assert response.json()['detail'][0]['msg'] == "field required"
