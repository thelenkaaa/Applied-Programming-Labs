from api import rental_api, user_api, car_api
from flask import Flask
from datetime import timedelta
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from database.schemas import UserSchema, CarSchema, OrderSchema
from database.manager import DBManager


# Create application.
app = Flask(__name__)
app.register_blueprint(car_api, url_prefix='/car')
app.register_blueprint(rental_api, url_prefix='/rental')
app.register_blueprint(user_api, url_prefix='/user')
CORS(app)

# Initialize JWT config.
ACCESS_EXPIRES = timedelta(hours=12)
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = ACCESS_EXPIRES
app.config['JWT_SECRET_KEY'] = '826cab9c02fe822a5a15be7f0296fd67'
jwt = JWTManager(app)

@jwt.user_identity_loader
def user_identity_lookup(username):
    return username


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    session = DBManager().session()
    record = session.query(UserSchema).filter(UserSchema.username == identity).first()
    return record


if __name__ == '__main__':
    app.run(port=63341)
