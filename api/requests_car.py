from flask_jwt_extended import jwt_required
from flask import Blueprint, request, make_response, Response
from marshmallow import ValidationError
from typing import List
import sqlalchemy.exc as sql_exception

from api.auth import user_api_authorize, admin_api_authorize
from api.schemas import CarCreation
from api.errors import BAD_REQUEST, OK
from database.schemas import CarSchema
import database.crud as db


car_api = Blueprint('car_api', 'car')


@car_api.route("", methods=["POST"])
@jwt_required()
@admin_api_authorize
def create_car() -> Response:
    request_json = request.get_json()

    try:
        # Validate request input.
        car = CarCreation().load(request_json)
        # Create database record.
        car_id = db.create_car(
            mark=car.get("mark"), category=car.get("category"), price=car.get("price"),
            transmission=car.get("transmission"), status=car.get("status")
        )
    except ValidationError as e:
        response = {
            "code": BAD_REQUEST,
            "message": f"Server crashed with the following error: {str(e)}"
        }
        return make_response(response, BAD_REQUEST)
    response = make_response({"carId": car_id}, OK)
    return response


@car_api.route("/<int:car_id>", methods=["PUT"])
@jwt_required()
@admin_api_authorize
def update_car(car_id) -> Response:
    request_json = request.get_json()

    car_record: CarSchema = db.get_car(car_id)
    if not car_record:
        response = {
            "code": BAD_REQUEST,
            "message": "There is no such id in database"
        }
        return make_response(response, BAD_REQUEST)

    try:
        # Validate request input.
        car = CarCreation().load(request_json)
        # Update database record.
        car_id = db.update_car(car_id=car_id, payload=car)
    except ValidationError as e:
        response = {
            "code": BAD_REQUEST,
            "message": f"Server crashed with the following error: {str(e)}"
        }
        return make_response(response, BAD_REQUEST)
    return make_response({"carId": car_id}, OK)


@car_api.route("/getAll", methods=["GET"])
@jwt_required()
@user_api_authorize
def get_all_cars() -> Response:
    # Get all filtered car records from db.
    cars: List[CarSchema] = db.get_cars()
    cars: List[dict] = list(map(lambda x: x.as_dict(), cars))
    return make_response(cars, OK)

@car_api.route("/getByStatusAvail", methods=["GET"])
@jwt_required()
@user_api_authorize
def get_car_by_status_avail() -> Response:

    # Get all filtered car records from db.
    cars: List[CarSchema] = db.get_cars_by_status(status="available")
    cars: List[dict] = list(map(lambda x: x.as_dict(), cars))
    return make_response(cars, OK)

@car_api.route("/getByStatusUnavail", methods=["GET"])
@jwt_required()
@user_api_authorize
def get_car_by_status_unavail() -> Response:

    # Get all filtered car records from db.
    cars: List[CarSchema] = db.get_cars_by_status(status="unavailable")
    cars: List[dict] = list(map(lambda x: x.as_dict(), cars))
    return make_response(cars, OK)


@car_api.route("/<car_id>", methods=["GET"])
def get_car(car_id) -> Response:
    car_record: CarSchema = db.get_car(car_id)
    if not car_record:
        response = {
            "code": BAD_REQUEST,
            "message": "There is no such id in database"
        }
        return make_response(response, BAD_REQUEST)
    return make_response(car_record.as_dict(), OK)


@car_api.route("/<car_id>", methods=["DELETE"])
@jwt_required()
@admin_api_authorize
def delete_car(car_id) -> Response:
    car_record: CarSchema = db.get_car(car_id)
    if not car_record:
        response = {
            "code": BAD_REQUEST,
            "message": "There is no such car"
        }
        return make_response(response, BAD_REQUEST)

    car_id = db.delete_car(car_id)
    return make_response({"carId": car_id}, OK)
