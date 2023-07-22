from typing import Dict, Optional, Mapping, Union
import json
import requests


def create_subscription(data: Dict) -> None:
    subscription_token = requests.get(
        "http://127.0.0.1:5000/check_user_subscription_email/123", timeout=3
    ).json().get('token', '')
    headers: Optional[Mapping[str, Union[str, bytes]]] = {
        "Content-Type": "application/json",
        "x-access-tokens": subscription_token,
    }

    payload = json.dumps(
        {
            "email": data.get("email"),
            "localization": data.get("localization"),
            "device_type": data.get("device_type"),
        }
    )
    requests.request(
        "POST",
        "http://127.0.0.1:5000/subscribe",
        headers=headers,
        data=payload,
        timeout=3,
    )


def check_subscription(email: str) -> Dict:
    subscription_token = requests.get(
        "http://127.0.0.1:5000/check_user_subscription_email/123", timeout=3
    ).json().get('token', '')
    headers: Optional[Mapping[str, Union[str, bytes]]] = {
        "Content-Type": "application/json",
        "x-access-tokens": subscription_token,
    }
    return requests.request(
        "GET",
        f"http://127.0.0.1:5000/check_user_email/{email}",
        headers=headers,
        timeout=3,
    ).json()
