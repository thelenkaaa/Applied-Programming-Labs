from unittest.mock import ANY
from api.errors import BAD_REQUEST, OK
from tests.utils import jwt_authentication_header
from tests.fixtures import *


def test_create_car(app_fixture, car_json_fixture, token_fixture):
    response = app_fixture.post(
        "/car",
        json=car_json_fixture,
        headers=jwt_authentication_header(token_fixture)
    )
    assert response.status_code == OK
    assert response.json.get("carId") == ANY

    test_db.delete_dummy_car(car_id=response.json.get("carId"))


def test_create_car_invalid_input(app_fixture, car_json_fixture, token_fixture):
    car_json_fixture["mark"] = 12
    response = app_fixture.post(
        "/car",
        json=car_json_fixture,
        headers=jwt_authentication_header(token_fixture)
    )
    assert response.status_code == BAD_REQUEST


def test_update_car(app_fixture, car_json_fixture, car_id_fixture, token_fixture):
    response = app_fixture.put(
        f"/car/{car_id_fixture}",
        json=car_json_fixture,
        headers=jwt_authentication_header(token_fixture)
    )
    assert response.status_code == OK
    assert response.json.get("carId") == ANY


def test_update_car_invalid_input(app_fixture, car_json_fixture, car_id_fixture, token_fixture):
    car_json_fixture["mark"] = 12
    response = app_fixture.put(
        f"/car/{car_id_fixture}",
        json=car_json_fixture,
        headers=jwt_authentication_header(token_fixture)
    )
    assert response.status_code == BAD_REQUEST


def test_get_car_by_status(app_fixture, car_json_fixture, token_fixture):
    response = app_fixture.get(
        f"/car/getByStatus",
        query_string={"status": car_json_fixture.get("status")},
        headers=jwt_authentication_header(token_fixture)
    )
    assert response.status_code == OK
    assert isinstance(response.json.get("cars"), list)


def test_get_car_by_status_invalid_input(app_fixture, token_fixture):
    response = app_fixture.get(
        f"/car/getByStatus",
        query_string={"status": "non-existing-status"},
        headers=jwt_authentication_header(token_fixture)
    )
    assert response.status_code == BAD_REQUEST


def test_get_car(app_fixture, car_id_fixture, token_fixture):
    response = app_fixture.get(
        f"/car/{car_id_fixture}",
        headers=jwt_authentication_header(token_fixture)
    )
    assert response.status_code == OK
    assert isinstance(response.json, dict)


def test_get_car_invalid_input(app_fixture, token_fixture):
    response = app_fixture.get(
        f"/car/{99999}",
        headers=jwt_authentication_header(token_fixture)
    )
    assert response.status_code == BAD_REQUEST


def test_delete_car(app_fixture, car_id_fixture, token_fixture):
    response = app_fixture.delete(
        f"/car/{car_id_fixture}",
        headers=jwt_authentication_header(token_fixture)
    )
    assert response.status_code == OK
    assert isinstance(response.json, dict)

    test_db.init_dummy_car()


def test_delete_car_invalid_input(app_fixture, token_fixture):
    response = app_fixture.delete(
        f"/car/{99999}",
        headers=jwt_authentication_header(token_fixture)
    )
    assert response.status_code == BAD_REQUEST
