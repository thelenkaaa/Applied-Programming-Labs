from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.orm import validates




Base = declarative_base()


class CarSchema(Base):
    __tablename__ = 'cars'
    car_id = Column(Integer, primary_key=True)
    mark = Column(String(255), nullable=False)
    category = Column(String(255), nullable=False)
    price = Column(Integer, nullable=False)
    transmission = Column(String(255), nullable=False)
    status = Column(String(255), nullable=False)
    # rental-service-bucket/images/image1.jpeg
    image_path = Column(String(255), nullable=False)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class UserSchema(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True)
    username = Column(String(10), unique=True, nullable=False)
    first_name = Column(String(10), nullable=False)
    last_name = Column(String(10), nullable=False)
    email = Column(String(20), nullable=False, unique=True)
    password = Column(String(20), nullable=False)
    phone = Column(Integer, nullable=False)
    drive_license = Column(String(1), nullable=False)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class OrderSchema(Base):
    __tablename__ = 'orders'

    order_id = Column(Integer, primary_key=True)
    renttime = Column(DateTime, nullable=False, default=datetime.utcnow)
    renttime_start = Column(DateTime, nullable=False, default=datetime.utcnow)
    renttime_end = Column(DateTime, nullable=False, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey(UserSchema.user_id))
    car_id = Column(Integer, ForeignKey(CarSchema.car_id))
    payment = Column(Integer, nullable=False)

    order1 = relationship(UserSchema, backref='orders', lazy="joined", foreign_keys=[user_id])
    order2 = relationship(CarSchema, backref='orders', lazy="joined", foreign_keys=[car_id])

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
