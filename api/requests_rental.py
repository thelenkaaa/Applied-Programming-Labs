from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import Blueprint, request, make_response, Response
from marshmallow import ValidationError
from typing import List
import sqlalchemy.exc as sql_exception

from api.auth import user_api_authorize, admin_api_authorize
from api.schemas import OrderCreation
from api.errors import BAD_REQUEST, OK
from database.schemas import OrderSchema, UserSchema
import database.crud as db


rental_api = Blueprint('rental', 'rental_api')


@rental_api.route("", methods=["POST"])
@jwt_required()
@user_api_authorize
def create_order() -> Response:
    request_json = request.get_json()

    username: str = get_jwt_identity()
    user: UserSchema = db.get_user(query_id=username, by=UserSchema.username)
    try:
        # Validate request input.
        order: dict = OrderCreation().load(request_json)
        # Create database record.
        order_id = db.create_order(user_id=user.user_id, car_id=order.get("car_id"), payment=order.get("payment"))
    except (ValidationError, sql_exception.IntegrityError) as e:
        response = {
            "code": BAD_REQUEST,
            "message": f"Server crashed with the following error: {str(e)}"
        }
        return make_response(response, BAD_REQUEST)
    return make_response({"orderId": order_id}, OK)


@rental_api.route("/<int:order_id>", methods=["GET"])
@jwt_required()
@user_api_authorize
def get_order(order_id) -> Response:
    order_record: OrderSchema = db.get_order(order_id)
    if not order_record:
        response = {
            "code": BAD_REQUEST,
            "message": "There is no such id in database"
        }
        return make_response(response, BAD_REQUEST)
    return make_response(order_record.as_dict(), OK)


@rental_api.route("/<int:order_id>", methods=["DELETE"])
@jwt_required()
@admin_api_authorize
def delete_order(order_id) -> Response:
    order_record: OrderSchema = db.get_order(order_id)
    if not order_record:
        response = {
            "code": BAD_REQUEST,
            "message": "There is no such id in database"
        }
        return make_response(response, BAD_REQUEST)

    order_id = db.delete_order(order_id)
    return make_response({"orderId": order_id}, OK)


@rental_api.route("/getRentedCars/<int:user_id>", methods=["GET"])
@jwt_required()
@user_api_authorize
def get_rented_cars(user_id) -> Response:
    orders: List[OrderSchema] = db.get_orders_by_userid(user_id=user_id)
    if not orders:
        response = {
            "code": BAD_REQUEST,
            "message": "There is no such id in database"
        }
        return make_response(response, BAD_REQUEST)

    cars: List[dict] = list(map(lambda x: (db.get_car(x.car_id)).as_dict(), orders))
    response = {
        "quantity": len(cars),
        "cars": cars
    }
    return make_response(response, OK)
