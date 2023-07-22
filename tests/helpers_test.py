import pytest
import requests
from unittest.mock import patch
from helpers.subscription import check_user_registration
from helpers.client import check_subscription, create_subscription


@patch("helpers.subscription.requests")
def test_check_user_registration_positive(mock_requests):
    # Mocking the first request to get the client token
    mock_requests.get.return_value.json.return_value = {"token": "mocked_client_token"}

    # Mocking the second request to check the user email
    mock_requests.request.return_value.json.return_value = {
        "status": "success",
        "message": "User exists",
    }

    # Test the function with a valid email
    result = check_user_registration("test@example.com")

    # Assert the expected output
    assert result == {"status": "success", "message": "User exists"}


@patch("helpers.subscription.requests")
def test_check_user_registration_negative(mock_requests):
    # Mocking the first request to get the client token
    mock_requests.get.return_value.json.return_value = {"token": "mocked_client_token"}

    # Mocking the second request to check the user email
    mock_requests.request.return_value.json.return_value = {
        "status": "error",
        "message": "User not found",
    }

    # Test the function with a non-existing email
    result = check_user_registration("non_existing@example.com")

    # Assert the expected output
    assert result == {"status": "error", "message": "User not found"}


@patch("helpers.subscription.requests")
def test_check_user_registration_token_failure(mock_requests):
    # Mocking the first request to get the client token with an exception
    mock_requests.get.side_effect = requests.exceptions.RequestException(
        "Failed to fetch token"
    )

    # Test the function with a valid email
    with pytest.raises(requests.exceptions.RequestException):
        check_user_registration("test@example.com")


@patch("helpers.client.requests")
def test_create_subscription_successful(mock_requests):
    # Mocking the request to get the subscription token
    mock_requests.get.return_value.json.return_value = {
        "token": "mocked_subscription_token"
    }

    # Test data for the subscription
    test_data = {
        "email": "test@example.com",
        "localization": "us",
        "device_type": "mobile",
    }

    # Test the function with valid subscription data
    create_subscription(test_data)

    # Assert that the POST request was made with the correct data and headers
    mock_requests.request.assert_called_once_with(
        "POST",
        "http://127.0.0.1:5000/subscribe",
        headers={
            "Content-Type": "application/json",
            "x-access-tokens": "mocked_subscription_token",
        },
        data='{"email": "test@example.com", "localization": "us", "device_type": "mobile"}',
        timeout=3,
    )


@patch("helpers.client.requests")
def test_create_subscription_token_failure(mock_requests):
    # Mocking the request to get the subscription token with an exception
    mock_requests.get.side_effect = requests.exceptions.RequestException(
        "Failed to fetch token"
    )

    # Test data for the subscription
    test_data = {
        "email": "test@example.com",
        "localization": "us",
        "device_type": "mobile",
    }

    # Test the function with valid subscription data but token failure
    with pytest.raises(requests.exceptions.RequestException):
        create_subscription(test_data)


@patch("helpers.client.requests")
def test_check_subscription_positive(mock_requests):
    # Mocking the request to get the subscription token
    mock_requests.get.return_value.json.return_value = {
        "token": "mocked_subscription_token"
    }

    # Mocking the request to check the user email with a successful response
    mock_requests.request.return_value.json.return_value = {
        "status": "success",
        "message": "Subscribed",
    }

    # Test the function with a valid email
    result = check_subscription("test@example.com")

    # Assert the expected output
    assert result == {"status": "success", "message": "Subscribed"}


@patch("helpers.client.requests")
def test_check_subscription_negative(mock_requests):
    # Mocking the request to get the subscription token
    mock_requests.get.return_value.json.return_value = {
        "token": "mocked_subscription_token"
    }

    # Mocking the request to check the user email with a failed response
    mock_requests.request.return_value.json.return_value = {
        "status": "error",
        "message": "Not subscribed",
    }

    # Test the function with a non-existing email
    result = check_subscription("non_existing@example.com")

    # Assert the expected output
    assert result == {"status": "error", "message": "Not subscribed"}


@patch("helpers.client.requests")
def test_check_subscription_token_failure(mock_requests):
    # Mocking the request to get the subscription token with an exception
    mock_requests.get.side_effect = requests.exceptions.RequestException(
        "Failed to fetch token"
    )

    # Test the function with a valid email
    with pytest.raises(requests.exceptions.RequestException):
        check_subscription("test@example.com")
