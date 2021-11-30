import datetime
from sqlalchemy.sql import func
from dataclasses import dataclass
from werkzeug.security import generate_password_hash, check_password_hash

from app import db
import uuid
from app.utils import IDEnum, StatusEnum


def generate_uuid():
    return str(uuid.uuid4())

@dataclass
class Retailer(db.Model):
    id: str
    phone_number: str
    first_name: str
    last_name: str
    id_type: str
    id_number: str
    pin: str
    status: str
    created: datetime.datetime
    modified: datetime.datetime

    __tablename__ = "retailer"
    id = db.Column(db.String(), primary_key=True, default=generate_uuid)
    phone_number = db.Column(db.String(), unique=True)
    first_name = db.Column(db.String(60), nullable=False)
    last_name = db.Column(db.String(60), nullable=False)
    id_type = db.Column(
        db.Enum(IDEnum, name="id_type"), default=IDEnum.national_id, nullable=False
    )
    id_number = db.Column(db.String(20), nullable=False)
    hash_pin = db.Column("pin", db.String(), nullable=False)
    status = db.Column(
        db.Enum(StatusEnum, name="status"), default=StatusEnum.inactive, nullable=False
    )
    created = db.Column(
        db.DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    modified = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    @property
    def pin(self):
        return self.hash_pin

    @pin.setter
    def pin(self, pin):
        self.hash_pin = generate_password_hash(pin, method="sha256")

    def verify_password(self, pin):
        return check_password_hash(self.hash_pin, pin)
