import database.crud as db


if __name__ == '__main__':
    user_id_1 = db.create_user(
        username="user", password="pass", first_name="user", last_name="user",
        email="user@gmail.com", phone="user", drive_license="B"
    )
    car_id_1 = db.create_car(mark="Lambo", category="SUV", price=1000, transmission="L", status="available")
    order_id_1 = db.create_order(user_id=user_id_1, car_id=car_id_1, payment=1000)

    user_id_2 = db.create_user(
        username="admin", password="pass", first_name="admin", last_name="admin",
        email="admin@gmail.com", phone="admin", drive_license="B"
    )
    car_id_2 = db.create_car(mark="Ferrari", category="Coupe", price=1000, transmission="L", status="available")
    order_id_2 = db.create_order(user_id=user_id_2, car_id=car_id_2, payment=1000)
