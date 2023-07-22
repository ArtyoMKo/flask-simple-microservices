import datetime
from functools import wraps
import uuid
from flask import Flask, request, jsonify, make_response
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import requests

from models.client import Users, db

app = Flask(__name__)

app.config["SECRET_KEY"] = "004f2af45d3a4e161a7dd2d17fdae47f"
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "sqlite:///client.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# db = SQLAlchemy(app)
db.init_app(app)

with app.app_context():
    db.create_all()

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

    existing_email = Users.query.filter_by(email=data.get('email')).first()
    if existing_email:
        return jsonify({'error': 'Email already registered'}), 409

    hashed_password = generate_password_hash(data.get("password"), method="sha256") if data.get("password") else ""

    new_user = Users(
        public_id=str(uuid.uuid4()),
        name=data.get("name"),
        email=data.get('email'),
        password=hashed_password,
        admin=False,
        localization=data.get('localization'),
        device_type=data.get('device_type')
    )

    db.session.add(new_user)
    db.session.commit()

    user_info = {
        'email': new_user.email,
        'device_type': new_user.device_type,
        'localization': new_user.localization
    }
    # response = requests.post("example.com", json=data)

    return jsonify({"message": "registeration successfully"})


@app.route('/check_user_id/<client_id>', methods=['GET'])
def check_user_by_id(client_id):
    client = Users.query.get(client_id)
    if not client:
        return jsonify({'error': 'Client not found', 'has_user': False, 'status': 404})

    return jsonify({'client_id': client.id, 'has_user': True, 'status': 200})


@app.route('/check_user_email/<client_email>', methods=['GET'])
def check_user_by_email(client_email):
    if not client_email:
        return jsonify({'error': 'Email not provided', 'has_user': False, 'status': 400})

    client = Users.query.filter_by(email=client_email).first()
    if not client:
        return jsonify({'error': 'Client not found', 'has_user': False, 'status': 404})

    return jsonify({'client_id': client.id, 'has_user': True, 'status': 200})


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