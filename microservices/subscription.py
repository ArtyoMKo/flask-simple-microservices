from functools import wraps
import os
from flask import Flask, request, jsonify
import jwt

from models.subscription import (
    Subscriptions,
    db,
    DefaultSubscriptions,
    create_and_populate_default_subscriptions_table,
)
from helpers.subscription import check_user_registration

app = Flask(__name__)

app.config["SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///subscription.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.app_context():
    db.create_all()
    create_and_populate_default_subscriptions_table(db)


# pylint:disable=duplicate-code
def token_required(funct):
    @wraps(funct)
    def decorator(*args, **kwargs):
        token = None

        if "x-access-tokens" in request.headers:
            token = request.headers["x-access-tokens"]

        if not token:
            return jsonify({"message": "a valid token is missing"})

        try:
            jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
        except:  # pylint:disable=bare-except
            return jsonify({"message": "token is invalid"})

        return funct(*args, **kwargs)

    return decorator


# This is not safe, it is just for task quick compleat
# The auth must be by some secret keys or by logged in checking
@app.route("/get_subscription_token/<request_id>", methods=["GET"])
def get_token(request_id):
    token = jwt.encode(
        {"request_id": request_id}, app.config["SECRET_KEY"], algorithm="HS256"
    )
    return jsonify({"token": token})


@app.route("/subscribe", methods=["POST"])
@token_required
def subscribe_user():
    data = request.get_json()

    existing_email = Subscriptions.query.filter_by(email=data.get("email")).first()
    if existing_email:
        return jsonify({"error": "Email already subscribed"}), 409

    response = check_user_registration(existing_email)

    if not response["has_user"]:
        return jsonify({"error": "Email do not exist"})

    row = DefaultSubscriptions.query.filter_by(
        device_type=data.get("device_type"), localization=data.get("localization")
    ).first()

    if not row.id:
        return jsonify(
            {
                "error": f"There is not defined subscription for localization|"
                f"{data.get('localization')} and device_type|{data.get('device_type')}"
            }
        )

    new_subscription = Subscriptions(
        sub_id=row.id,
        name=data.get("name"),
        email=data.get("email"),
        localization=data.get("localization"),
        device_type=data.get("device_type"),
    )

    db.session.add(new_subscription)
    db.session.commit()

    return jsonify({"message": "Subscription created successfully"})


@app.route("/check_user_subscription_email/<client_email>", methods=["GET"])
@token_required
def check_user_subscription_by_email(client_email):
    if not client_email:
        return jsonify(
            {"error": "Email not provided", "has_user": False, "status": 400}
        )

    client = Subscriptions.query.filter_by(email=client_email).first()
    if not client:
        return jsonify(
            {"error": "Client not found", "has_subscription": False, "status": 404}
        )

    return jsonify({"client_id": client.id, "has_subscription": True, "status": 200})


if __name__ == "__main__":
    app.run(debug=True)
