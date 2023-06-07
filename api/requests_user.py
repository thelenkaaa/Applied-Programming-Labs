from flask_jwt_extended import create_access_token, jwt_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Blueprint, request, make_response, Response
from sqlalchemy.exc import IntegrityError
from marshmallow import ValidationError
import sqlalchemy.exc as sql_exception

from api.auth import user_api_authorize
from database.schemas import *
from api.schemas import UserCreation, UserInfo
from api.errors import BAD_REQUEST, NOT_AUTHORIZED, OK
import database.crud as db
from typing import Optional


user_api = Blueprint('user', 'user_api')


def compose_response(code: int, message: Optional[str] = None, data: Optional[dict] = None):
    response = {
        "status": code,
        "statusText": message if message else "",
        "data": data if data else {}
    }
    return response

@user_api.route('/user', methods=['POST'])
def create_user():
    request_json = request.get_json()

    try:
        # Validate input.
        new_user = UserCreation().load(request_json)

        if db.is_username_taken(new_user['username']):
            return make_response(compose_response(
                code=BAD_REQUEST,
                message='Username already exists'), BAD_REQUEST)
        # Create a new DB record.
        user_record: UserSchema = db.create_user(
            username=new_user.get('username'),
            password=new_user.get('password'),
            first_name=new_user.get('first_name'),
            last_name=new_user.get('last_name'),
            email=new_user.get('email'),
            phone=new_user.get('phone'),
            drive_license=new_user.get('drive_license')
        )
    except (ValidationError, sql_exception.IntegrityError) as e:
        return make_response(compose_response(
              code=BAD_REQUEST,
              message=f"Server crashed with following error: {e}"), BAD_REQUEST)
    except IntegrityError:
        return make_response(compose_response(
            code=BAD_REQUEST,
            message='Username already exists'), BAD_REQUEST)
    return make_response(compose_response(
        code=OK,
        message='Signup is successful',
        data={"userId": user_record.user_id}), OK)



@user_api.route('/login', methods=['POST'])
def login_user():
    username = request.json['username']
    password = request.json['password']

    # Check if such user exists. If so, generate JWT token and send it back to user.
    user: UserSchema = db.get_user(query_id=username, by=UserSchema.username)
    if user and check_password_hash(user.password, password):
        access_token = create_access_token(identity=user.username)
        return make_response(compose_response(
        code=OK,
        data={"AccessToken": access_token}), OK)
    else:
        return make_response(compose_response(
              code=NOT_AUTHORIZED,
              message="Invalid login or password."), BAD_REQUEST)


@user_api.route("/logout", methods=['DELETE'])
@jwt_required()
@user_api_authorize
def logout():
    return make_response({"msg": "Successfully logged out"}, OK)


@user_api.route("/me", methods=["GET"])
@jwt_required()
@user_api_authorize
def get_user() -> Response:

    user_record: UserSchema = current_user

    if not user_record:
        response = {
            "code": BAD_REQUEST,
            "message": "There is no such id in database"
        }
        return make_response(response, BAD_REQUEST)
    return make_response(UserInfo().dump(user_record), OK)


@user_api.route("/updateMe", methods=["PUT"])
@jwt_required()
@user_api_authorize
def update_user() -> Response:
    request_json = request.get_json()

    user_record: UserSchema = current_user

    if not user_record:
        response = {
            "code": BAD_REQUEST,
            "message": "There is no such user"
        }
        return make_response(response, BAD_REQUEST)

    try:
        user = request_json
        # Update database record.
        user_id = db.update_user(
            user_id=user_record.user_id,
            username=user.get('username'),
            first_name=user.get('name'),
            last_name=user.get('surname'),
            email=user.get('email'),
            password=user.get('password') and generate_password_hash(user.get('password')),
            phone=user.get('phone'),
            drive_license=user.get('drive_license')
        )
    except ValidationError as e:
        return make_response(compose_response(
              code=BAD_REQUEST,
              message=f"Validation error: {str(e)}"), BAD_REQUEST)
    except sql_exception.IntegrityError as e:
        return make_response(compose_response(
              code=BAD_REQUEST,
              message=f"Server crashed with the following error: {str(e)}"), BAD_REQUEST)
    return make_response(compose_response(
        code=OK,
        message='Edit is successful',
        data={"userId": user_id}), OK)


# @user_api.route("/updateMe", methods=["PUT"])
# @jwt_required()
# @user_api_authorize
# def update_user() -> Response:
#     user_id: UserSchema = current_user.user_id
#
#     if not user_id:
#         response = {
#             "code": BAD_REQUEST,
#             "message": "There is no such user"
#         }
#         return make_response(response, BAD_REQUEST)
#
#     if not request.is_json:
#         response = {
#             "code": BAD_REQUEST,
#             "message": "Request payload must be a JSON object"
#         }
#         return make_response(response, BAD_REQUEST)
#
#     user_data = request.get_json()
#
#     user_schema = UserSchema()
#     errors = user_schema.validate(user_data)
#     if errors:
#         response = {
#             "code": BAD_REQUEST,
#             "message": "Invalid request payload",
#             "errors": errors
#         }
#         return make_response(response, BAD_REQUEST)
#
#     user_id = db.update_user(
#         user_id=user_id,
#         username=user_data.get('username'),
#         first_name=user_data.get('name'),
#         last_name=user_data.get('surname'),
#         email=user_data.get('email'),
#         password=generate_password_hash(user_data.get('password')) if user_data.get('password') else None,
#         phone=user_data.get('phone'),
#         drive_license=user_data.get('drive_license')
#     )
#
#     return make_response({"userId": user_id}, OK)


@user_api.route("/deleteMe", methods=["DELETE"])
@jwt_required()
@user_api_authorize
def delete_user() -> Response:
    user_id: UserSchema = current_user.user_id

    if not user_id:
        response = {
            "code": BAD_REQUEST,
            "message": "There is no such user"
        }
        return make_response(response, BAD_REQUEST)

    user_id = db.delete_user(user_id)
    return make_response({"userId": user_id}, OK)

# @user_api.route("/<user_id>", methods=["DELETE"])
# @jwt_required()
# @user_api_authorize
# def delete_user(user_id) -> Response:
#     user_record: UserSchema = db.get_user(user_id)
#     if not user_record:
#         response = {
#             "code": BAD_REQUEST,
#             "message": "There is no such user"
#         }
#         return make_response(response, BAD_REQUEST)
#
#     user_id = db.delete_user(user_id)
#     return make_response({"userId": user_id}, OK)
