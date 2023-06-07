TEST_CAR = {
    "car_id": 1000,
    "mark": "Toyota",
    "category": "SUV",
    "price": 10000,
    "transmission": "L",
    "status": "available"
}

TEST_USER = {
    "user_id":       1000,
    "username":      "test_user",
    "first_name":    "test",
    "last_name":     "test",
    "email":         "test@gmail.com",
    "password":      "pass",
    "phone":         "test",
    "drive_license": "B"
}

TEST_ADMIN_USER = {
    "user_id":       1001,
    "username":      "admin",
    "first_name":    "admin",
    "last_name":     "admin",
    "email":         "admin@gmail.com",
    "password":      "pass",
    "phone":         "admin",
    "drive_license": "B"
}

TEST_ORDER = {
    "order_id": 1000,
    "payment": 1442,
    "user_id": TEST_USER.get("user_id"),
    "car_id": TEST_CAR.get("car_id")
}
