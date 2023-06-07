from werkzeug.security import generate_password_hash
from database.manager import DBManager
from database.schemas import UserSchema, OrderSchema, CarSchema
from flask.testing import FlaskClient
import tests.database.test_config as test_config
import copy


def login_user(client: FlaskClient, user_payload: dict):
    response = client.get(
        "/user/login",
        auth=(user_payload['username'], user_payload['password'])
    )
    return response.json['AccessToken']


def create_dummy_user(user_payload: dict) -> int:
    session = DBManager().session()

    test_user: dict = copy.deepcopy(user_payload)
    test_user["password"] = generate_password_hash(test_user.get("password"))
    user = UserSchema(**test_user)
    user_id = copy.copy(user.user_id)

    session.add(user)
    session.commit()
    session.close()
    return user_id


def delete_dummy_user(user_payload: dict) -> int:
    session = DBManager().session()

    session.query(OrderSchema).filter(user_payload.get("user_id") == OrderSchema.user_id).delete()
    session.query(UserSchema).filter(user_payload.get("user_id") == UserSchema.user_id).delete()

    session.commit()
    session.close()
    return user_payload.get("user_id")


def init_dummy_user(user_payload: dict = test_config.TEST_USER):
    delete_dummy_user(user_payload)
    create_dummy_user(user_payload)


def create_dummy_car(car_payload: dict = test_config.TEST_CAR) -> int:
    session = DBManager().session()

    car = CarSchema(**car_payload)
    car_id = copy.copy(car.car_id)

    session.add(car)
    session.commit()
    session.close()
    return car_id


def delete_dummy_car(car_payload: dict = None, car_id: int = None) -> int:
    car_id = car_id if car_id else car_payload.get("car_id")

    session = DBManager().session()
    session.query(OrderSchema).filter(car_id == OrderSchema.car_id).delete()
    session.query(CarSchema).filter(car_id == CarSchema.car_id).delete()

    session.commit()
    session.close()
    return car_id


def init_dummy_car(car_payload: dict = test_config.TEST_CAR):
    delete_dummy_car(car_payload)
    create_dummy_car(car_payload)


def create_dummy_order(order_payload: dict = test_config.TEST_ORDER) -> int:
    session = DBManager().session()
    order = OrderSchema(**order_payload)
    session.add(order)
    session.commit()
    session.close()
    return order_payload.get("order_id")


def delete_dummy_order(order_payload: dict = None, order_id: int = None) -> int:
    order_id = order_id if order_id else order_payload.get("order_id")

    session = DBManager().session()
    session.query(OrderSchema).filter(order_id == OrderSchema.order_id).delete()
    session.commit()
    session.close()
    return order_id


def init_dummy_order(order_payload: dict = test_config.TEST_ORDER):
    delete_dummy_order(order_payload)
    create_dummy_order(order_payload)
