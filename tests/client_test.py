# test_app.py

import pytest
from microservices.client import app, db
from models.client import Users


@pytest.fixture
def client():
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['TESTING'] = True
    with app.app_context():
        db.create_all()

    with app.test_client() as client:
        yield client

    with app.app_context():
        db.drop_all()


# Test client signup
def test_signup(client):
    # Prepare test data
    data = {
        "password": "12121212121",
        "name": "Test Name",
        "email": "test@mail.com",
        "localization": "am",
        "device_type": "ios"
    }

    # Send POST request to signup endpoint
    response = client.post('/register', json=data)

    # Check response status code and content
    assert response.status_code == 200
    assert response.json == {'message': 'registeration successfully'}

    # Check if the client is saved in the database
    client = Users.query.filter_by(email=data['email']).first()
    assert client is not None
    assert client.email == data['email']
    assert client.password != data['password']
    assert client.name == data['name']
    assert client.localization == data['localization']
    assert client.device_type == data['device_type']
