from app import app
import tests.database.test_config as test_config
import tests.database.db as test_db
import pytest


AUTH_TOKEN = None


@pytest.fixture(scope="session", autouse=True)
def init():
    """
    This function is executed before the actual tests
    to initialize test database records.
    :return: None
    """
    global AUTH_TOKEN

    with app.app_context():
        with app.test_client() as client:
            test_db.init_dummy_car(car_payload=test_config.TEST_CAR)
            test_db.init_dummy_user(user_payload=test_config.TEST_USER)
            test_db.init_dummy_user(user_payload=test_config.TEST_ADMIN_USER)
            test_db.init_dummy_order(order_payload=test_config.TEST_ORDER)
            AUTH_TOKEN = test_db.login_user(client=client, user_payload=test_config.TEST_ADMIN_USER)


@pytest.fixture()
def app_fixture():
    new_app = app
    new_app.config['TESTING'] = True

    with new_app.app_context():
        with new_app.test_client() as client:
            yield client


@pytest.fixture()
def token_fixture():
    global AUTH_TOKEN
    return AUTH_TOKEN


@pytest.fixture()
def user_json_fixture():
    return {
        "username": test_config.TEST_USER.get("username"),
        "first_name": test_config.TEST_USER.get("first_name"),
        "last_name": test_config.TEST_USER.get("last_name"),
        "email": test_config.TEST_USER.get("email"),
        "password": test_config.TEST_USER.get("password"),
        "phone": test_config.TEST_USER.get("phone"),
        "drive_license": test_config.TEST_USER.get("drive_license")
    }


@pytest.fixture()
def user_id_fixture():
    return test_config.TEST_USER.get("user_id")


@pytest.fixture()
def car_json_fixture():
    return {
        "mark": test_config.TEST_CAR.get("mark"),
        "category": test_config.TEST_CAR.get("category"),
        "price": test_config.TEST_CAR.get("price"),
        "transmission": test_config.TEST_CAR.get("transmission"),
        "status": test_config.TEST_CAR.get("status")
    }


@pytest.fixture()
def car_id_fixture():
    return test_config.TEST_CAR.get("car_id")


@pytest.fixture()
def order_json_fixture():
    return {
        "payment": test_config.TEST_ORDER.get("payment"),
        "car_id": test_config.TEST_ORDER.get("car_id")
    }


@pytest.fixture()
def order_id_fixture():
    return test_config.TEST_ORDER.get("order_id")


@pytest.fixture()
def order_user_id_fixture():
    return test_config.TEST_ORDER.get("user_id")
