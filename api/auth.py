from api.errors import BAD_REQUEST, NOT_AUTHORIZED
from database.config import ADMIN
from database.schemas import UserSchema
import database.crud as db

from flask_jwt_extended import get_jwt_identity
from flask import make_response


def user_api_authorize(func):
    def verify_jwt(*args, **kwargs):
        identity: str = get_jwt_identity()
        user_record: UserSchema = db.get_user(query_id=identity, by=UserSchema.username)

        # Check if such user exists.
        if not user_record:
            response = {
                "code": BAD_REQUEST,
                "message": f"User [{identity}] does not exist."
            }
            return make_response(response, BAD_REQUEST)

        # Validate JWT token.
        if identity not in [user_record.username, ADMIN]:
            response = {
                "code": NOT_AUTHORIZED,
                "message": f"User [{identity}] is not allowed to do this action."
            }
            return make_response(response, NOT_AUTHORIZED)
            
        return func(*args, **kwargs)

    verify_jwt.__name__ = func.__name__
    return verify_jwt


def admin_api_authorize(func):
    def verify_jwt_admin(*args, **kwargs):
        identity = get_jwt_identity()

        # Validate JWT token.
        if identity not in [ADMIN]:
            response = {
                "code": NOT_AUTHORIZED,
                "message": f"Only admins can execute this action. User [{identity}] is not an admin."
            }
            return make_response(response, NOT_AUTHORIZED)
        return func(*args, **kwargs)

    verify_jwt_admin.__name__ = func.__name__
    return verify_jwt_admin
