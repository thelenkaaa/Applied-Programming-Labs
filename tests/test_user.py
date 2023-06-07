from unittest.mock import ANY
from api.errors import BAD_REQUEST, NOT_AUTHORIZED, OK
from tests.utils import jwt_authentication_header
from tests.fixtures import *
import random


def test_create_user(app_fixture, user_json_fixture):
    user_json_fixture["username"] = f"test_{random.randint(0, 10000)}"
    user_json_fixture["email"] = f"test_{random.randint(0, 10000)}"

    response = app_fixture.post(
        "/user",
        json=user_json_fixture
    )
    assert response.status_code == OK
    assert response.json.get("userId") == ANY

    test_db.delete_dummy_user(user_payload=response.json)


def test_create_user_validation_failure(app_fixture, user_json_fixture):
    user_json_fixture["username"] = 10000

    response = app_fixture.post(
        "/user",
        json=user_json_fixture
    )
    assert response.status_code == BAD_REQUEST


def test_create_user_sql_failure(app_fixture, user_json_fixture):
    user_json_fixture["username"] = "admin"
    response = app_fixture.post(
        "/user",
        json=user_json_fixture
    )
    assert response.status_code == BAD_REQUEST


def test_login_user(app_fixture, user_json_fixture):
    response = app_fixture.get(
        "/user/login",
        auth=(user_json_fixture.get("username"), user_json_fixture.get("password"))
    )
    assert response.status_code == OK
    assert response.json.get("AccessToken") == ANY


def test_login_user_invalid_creds(app_fixture, user_json_fixture):
    response = app_fixture.get(
        "/user/login",
        auth=("some-random-username", user_json_fixture.get("password"))
    )
    assert response.status_code == BAD_REQUEST

    response = app_fixture.get(
        "/user/login",
        auth=("", user_json_fixture.get("password"))
    )
    assert response.status_code == NOT_AUTHORIZED


def test_logout(app_fixture, token_fixture):
    response = app_fixture.delete(
        "/user/logout",
        headers=jwt_authentication_header(token_fixture)
    )
    assert response.status_code == OK


def test_get_valid_user(app_fixture, user_id_fixture, token_fixture):
    response = app_fixture.get(
        f"/user/{user_id_fixture}",
        headers=jwt_authentication_header(token_fixture)
    )
    assert response.status_code == OK
    assert isinstance(response.json, dict)


def test_get_invalid_user(app_fixture, token_fixture):
    response = app_fixture.get(
        f"/user/{99999}",
        headers=jwt_authentication_header(token_fixture)
    )
    assert response.status_code == BAD_REQUEST


def test_update_valid_user(app_fixture, user_id_fixture, user_json_fixture, token_fixture):
    response = app_fixture.put(
        f"/user/{user_id_fixture}",
        headers=jwt_authentication_header(token_fixture),
        json=user_json_fixture
    )
    assert response.status_code == OK
    assert response.json.get("userId") == ANY


def test_update_invalid_user(app_fixture, user_id_fixture, user_json_fixture, token_fixture):
    wrong_sql_update_payload = user_json_fixture
    wrong_sql_update_payload["username"] = "admin"

    response = app_fixture.put(
        f"/user/{99999}",
        headers=jwt_authentication_header(token_fixture)
    )
    assert response.status_code == BAD_REQUEST

    response = app_fixture.put(
        f"/user/{user_id_fixture}",
        headers=jwt_authentication_header(token_fixture),
        json=wrong_sql_update_payload
    )
    assert response.status_code == BAD_REQUEST


def test_delete_valid_user(app_fixture, user_id_fixture, token_fixture):
    response = app_fixture.delete(
        f"/user/{user_id_fixture}",
        headers=jwt_authentication_header(token_fixture)
    )
    assert response.status_code == OK
    assert response.json.get('user_id') == ANY

    test_db.init_dummy_user(user_payload=test_config.TEST_USER)


def test_delete_invalid_user(app_fixture, token_fixture):
    response = app_fixture.delete(
        f"/user/{99999}",
        headers=jwt_authentication_header(token_fixture)
    )
    assert response.status_code == BAD_REQUEST
