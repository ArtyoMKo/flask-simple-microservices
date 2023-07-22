# mypy: ignore-errors
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.Integer)
    name = db.Column(db.String(50))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(50))
    admin = db.Column(db.Boolean)
    localization = db.Column(db.String(50), nullable=False)
    device_type = db.Column(db.String(20), nullable=False)

    # pylint:disable=too-many-arguments
    def __init__(
        self, public_id, name, email, password, admin, localization, device_type
    ):
        self.public_id = public_id
        self.name = name
        self.email = email
        self.password = password
        self.admin = admin
        self.localization = localization
        self.device_type = device_type
