import datetime
from functools import wraps
import uuid
from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import jwt


app = Flask(__name__)

app.config["SECRET_KEY"] = "004f2af45d3a4e161a7dd2d17fdae47f"
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "sqlite://///home/manthantrivedi/Documents/Bacancy/bacancy_blogs/flask_auth/\
myflaskproject/bookstore.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

db = SQLAlchemy(app)

from models.client import Users


def token_required(funct):
    @wraps(funct)
    def decorator(*args, **kwargs):
        token = None

        if "x-access-tokens" in request.headers:
            token = request.headers["x-access-tokens"]

        if not token:
            return jsonify({"message": "a valid token is missing"})

        try:
            data = jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
            current_user = Users.query.filter_by(public_id=data["public_id"]).first()
        except:
            return jsonify({"message": "token is invalid"})

        return funct(current_user, *args, **kwargs)

    return decorator


@app.route("/register", methods=["POST"])
def signup_user():
    data = request.get_json()

    hashed_password = generate_password_hash(data["password"], method="sha256")

    new_user = Users(
        public_id=str(uuid.uuid4()),
        name=data["name"],
        password=hashed_password,
        admin=False,
    )
    db.session.add(new_user)
    db.session.commit()

    # todo Create subscription and check subscription condition

    return jsonify({"message": "registeration successfully"})


@app.route("/login", methods=["POST"])
def login_user():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return make_response(
            "could not verify", 401, {"Authentication": 'login required"'}
        )

    user = Users.query.filter_by(name=auth.username).first()

    if check_password_hash(user.password, auth.password):
        token = jwt.encode(
            {
                "public_id": user.public_id,
                "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=45),
            },
            app.config["SECRET_KEY"],
            "HS256",
        )
        return jsonify({"token": token})

    return make_response(
        "could not verify", 401, {"Authentication": '"login required"'}
    )


if __name__ == "__main__":
    app.run(debug=True)
