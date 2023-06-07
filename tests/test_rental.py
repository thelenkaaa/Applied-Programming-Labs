from unittest.mock import ANY
from api.errors import BAD_REQUEST, OK
from tests.utils import jwt_authentication_header
from tests.fixtures import *


def test_create_order(app_fixture, order_json_fixture, token_fixture):
    response = app_fixture.post(
        "/rental",
        json=order_json_fixture,
        headers=jwt_authentication_header(token_fixture)
    )
    assert response.status_code == OK
    assert response.json.get("orderId") == ANY

    test_db.delete_dummy_order(order_id=response.json.get("orderId"))


def test_create_order_invalid_input(app_fixture, order_json_fixture, token_fixture):
    order_json_fixture["payment"] = "payment"
    response = app_fixture.post(
        "/rental",
        json=order_json_fixture,
        headers=jwt_authentication_header(token_fixture)
    )
    assert response.status_code == BAD_REQUEST

    order_json_fixture["car_id"] = 999999
    response = app_fixture.post(
        "/rental",
        json=order_json_fixture,
        headers=jwt_authentication_header(token_fixture)
    )
    assert response.status_code == BAD_REQUEST


def test_get_order(app_fixture, order_id_fixture, token_fixture):
    response = app_fixture.get(
        f"/rental/{order_id_fixture}",
        headers=jwt_authentication_header(token_fixture)
    )
    assert response.status_code == OK
    assert isinstance(response.json, dict)


def test_get_order_invalid_input(app_fixture, token_fixture):
    response = app_fixture.get(
        f"/rental/{99999}",
        headers=jwt_authentication_header(token_fixture)
    )
    assert response.status_code == BAD_REQUEST


def test_get_rented_cars(app_fixture, order_user_id_fixture, token_fixture):
    response = app_fixture.get(
        f"/rental/getRentedCars/{order_user_id_fixture}",
        headers=jwt_authentication_header(token_fixture)
    )
    assert response.status_code == OK
    assert isinstance(response.json.get("quantity"), int)


def test_get_rented_cars_invalid_input(app_fixture, token_fixture):
    response = app_fixture.get(
        f"/rental/getRentedCars/{99999}",
        headers=jwt_authentication_header(token_fixture)
    )
    assert response.status_code == BAD_REQUEST


def test_delete_order(app_fixture, order_id_fixture, token_fixture):
    response = app_fixture.delete(
        f"/rental/{order_id_fixture}",
        headers=jwt_authentication_header(token_fixture)
    )
    assert response.status_code == OK
    assert response.json.get("orderId") == ANY

    test_db.init_dummy_order()


def test_delete_order_invalid_input(app_fixture, token_fixture):
    response = app_fixture.delete(
        f"/rental/{99999}",
        headers=jwt_authentication_header(token_fixture)
    )
    assert response.status_code == BAD_REQUEST
