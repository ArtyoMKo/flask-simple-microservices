# mypy: ignore-errors
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


# type: ignore
class Subscriptions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sub_id = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(50))
    email = db.Column(db.String(100), unique=True)
    localization = db.Column(db.String(50), nullable=False)
    device_type = db.Column(db.String(20), nullable=False)

    # pylint:disable=too-many-arguments
    def __init__(self, sub_id, name, email, localization, device_type):
        self.sub_id = sub_id
        self.name = name
        self.email = email
        self.localization = localization
        self.device_type = device_type


class DefaultSubscriptions(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True)
    name = db.Column(db.String(50))
    localization = db.Column(db.String(50), nullable=False)
    device_type = db.Column(db.String(20), nullable=False)

    __table_args__ = (
        db.UniqueConstraint(
            "name", "localization", "device_type", name="_column1_column2_uc"
        ),
    )

    def __init__(self, name, localization, device_type):
        self.name = name
        self.localization = localization
        self.device_type = device_type


def create_and_populate_default_subscriptions_table(database_object):
    if not DefaultSubscriptions.query.all():
        default_subscriptions = [
            DefaultSubscriptions(name="sub1", localization="am", device_type="ios"),
            DefaultSubscriptions(name="sub2", localization="en", device_type="ios"),
            DefaultSubscriptions(name="sub3", localization="en", device_type="android"),
        ]

        database_object.session.bulk_save_objects(default_subscriptions)
        database_object.session.commit()
