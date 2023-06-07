from database.schemas import UserSchema, CarSchema, OrderSchema
from database.manager import DBManager
from werkzeug.security import generate_password_hash
from typing import Union, List
import random
import copy


def get_user(query_id: Union[int, str], by=UserSchema.user_id) -> UserSchema:
    session = DBManager().session()
    record = session.query(UserSchema).filter(by == query_id).first()
    record = copy.deepcopy(record)
    session.close()
    return record

def is_username_taken(username):
    session = DBManager().session()
    # Query the database to check if the username exists
    user = session.query(UserSchema).filter_by(username=username).first()
    return user is not None

def get_user_by_username(query_id, by=UserSchema.username) -> UserSchema:
    print('jcnfvdklvfkmw')
    print(query_id)

    session = DBManager().session()
    print(query_id)
    record = session.query(UserSchema).filter(UserSchema.username == query_id).first()
    record = copy.deepcopy(record)
    session.close()
    return record


def get_car(query_id: Union[int, str], by=CarSchema.car_id) -> CarSchema:
    session = DBManager().session()
    record = session.query(CarSchema).filter(by == query_id).first()
    record = copy.deepcopy(record)
    session.close()
    return record


def get_order(query_id: Union[int, str], by=OrderSchema.order_id) -> CarSchema:
    session = DBManager().session()
    record = session.query(OrderSchema).filter(by == query_id).first()
    record = copy.deepcopy(record)
    session.close()
    return record


def update_user(
        user_id: int,
        username: str = None,
        first_name: str = None,
        last_name: str = None,
        email: str = None,
        password: str = None,
        phone: int = None,
        drive_license: str = None
) -> int:
    session = DBManager().session()
    # Update record.
    user_record = {}

    user_record.update({"username": username} if username else {})
    user_record.update({"first_name": first_name} if first_name else {})
    user_record.update({"last_name": last_name} if last_name else {})

    # Generate password hash using SHA256 algorithm.
    user_record.update({"email": email} if email else {})
    password_hash = generate_password_hash(password) if password else None
    user_record.update({"password": password_hash} if password else {})
    user_record.update({"phone": phone} if phone else {})
    user_record.update({"drive_license": drive_license} if drive_license else {})

    session.query(UserSchema).filter(UserSchema.user_id == user_id).update(user_record)
    session.commit()
    session.close()
    return user_id


def create_user(
        username: str, password: str, first_name: str, last_name: str, email: str, phone: str, drive_license: str
) -> UserSchema:
    session = DBManager().session()
    # Generate password hash using SHA256 algorithm.
    password_hash = generate_password_hash(password)
    # Add record.
    user_record = UserSchema(
        user_id=random.randint(1, 10000),
        username=username,
        password=password_hash,
        first_name=first_name,
        last_name=last_name,
        email=email,
        phone=phone,
        drive_license=drive_license
    )
    record = copy.deepcopy(user_record)

    session.add(user_record)
    session.commit()
    session.close()
    return record


def delete_user(user_id: int):
    session = DBManager().session()
    session.query(OrderSchema).filter(OrderSchema.user_id == user_id).delete()
    session.query(UserSchema).filter(UserSchema.user_id == user_id).delete()
    session.commit()
    # session.close()
    return user_id


def create_car(mark: str, category: str, price: int, transmission: str, status: str) -> int:
    session = DBManager().session()
    car_record = CarSchema(
        car_id=random.randint(1, 10000),
        mark=mark,
        category=category,
        price=price,
        transmission=transmission,
        status=status
    )
    car_id = copy.deepcopy(car_record.car_id)
    session.add(car_record)
    session.commit()
    session.close()
    return car_id


def update_car(car_id: int, payload: dict) -> int:
    session = DBManager().session()
    session.query(CarSchema).filter(car_id == CarSchema.car_id).update(payload)
    session.commit()
    session.close()
    return car_id


def get_cars_by_status(status: str) -> List[CarSchema]:
    session = DBManager().session()
    cars: List[CarSchema] = session.query(CarSchema).filter(status == CarSchema.status).all()
    cars = copy.deepcopy(cars)
    session.close()
    return cars

def get_cars() -> List[CarSchema]:
    session = DBManager().session()
    cars: List[CarSchema] = session.query(CarSchema).all()
    cars = copy.deepcopy(cars)
    session.close()
    return cars


def delete_car(car_id: int) -> int:
    session = DBManager().session()
    session.query(OrderSchema).filter(OrderSchema.car_id == car_id).delete()
    session.query(CarSchema).filter(CarSchema.car_id == car_id).delete()
    session.commit()
    session.close()
    return car_id


def create_order(user_id: int, car_id: int, payment: int) -> int:
    session = DBManager().session()
    order_record = OrderSchema(
        order_id=random.randint(1, 10000),
        user_id=user_id,
        car_id=car_id,
        payment=payment,
    )
    order_id = copy.deepcopy(order_record.order_id)
    session.add(order_record)
    session.commit()
    session.close()
    return order_id


def delete_order(order_id: int) -> int:
    session = DBManager().session()
    session.query(OrderSchema).filter(OrderSchema.order_id == order_id).delete()
    session.commit()
    session.close()
    return order_id


def get_orders_by_userid(user_id: int) -> List[OrderSchema]:
    session = DBManager().session()
    orders: List[OrderSchema] = session.query(OrderSchema).filter(OrderSchema.user_id == user_id).all()
    orders = copy.deepcopy(orders)
    session.close()
    return orders
