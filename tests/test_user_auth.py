from api.errors import BAD_REQUEST, NOT_AUTHORIZED
from tests.utils import jwt_authentication_header
from flask_jwt_extended import create_access_token
from tests.fixtures import *


def generate_jwt_token(username):
    ctx = app.app_context()
    ctx.push()
    access_token = create_access_token(identity=username)
    ctx.pop()
    return access_token


def test_user_verify_jwt_wrong_credentials(app_fixture, user_id_fixture, token_fixture):
    wrong_token = generate_jwt_token(username="invalid-username")

    response = app_fixture.get(
        f"/user/{user_id_fixture}",
        headers=jwt_authentication_header(wrong_token)
    )
    assert response.status_code == BAD_REQUEST


def test_admin_verify_jwt_wrong_credentials(app_fixture, user_json_fixture, order_id_fixture, token_fixture):
    token = test_db.login_user(app_fixture, user_json_fixture)

    response = app_fixture.delete(
        f"/rental/{order_id_fixture}",
        headers=jwt_authentication_header(token)
    )
    assert response.status_code == NOT_AUTHORIZED
