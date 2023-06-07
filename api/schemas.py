from marshmallow import Schema, fields, validate
from flask_marshmallow import Marshmallow
ma = Marshmallow()

CAR_STATUSES = ['available', 'unavailable']


class CarCreation(Schema):
    mark = fields.String(metadata={"validator": validate.Length(min=1, max=60)})
    category = fields.String(metadata={"validator": validate.Length(min=1, max=60)})
    price = fields.Integer(
        validate=[validate.Range(min=0, min_inclusive=True, error="Car price should be >= 0.")]
    )
    transmission = fields.String()
    status = fields.String(metadata={"validator": validate.OneOf(CAR_STATUSES)})
    image_path = fields.String()



class OrderCreation(Schema):
    car_id = fields.Integer()
    payment = fields.Integer()


class UserInfo(Schema):
    user_id = fields.Integer()
    username = fields.String()
    first_name = fields.String()
    last_name = fields.String()
    email = fields.String(metadata={"validator": validate.Email()})
    phone = fields.Integer()
    drive_license = fields.String()


class UserCreation(UserInfo):
    password = fields.String()
