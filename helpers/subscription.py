from typing import Dict, Optional, Mapping, Union
import json
import requests


def check_user_registration(email: str) -> Dict:
    client_token = (
        requests.get("http://127.0.0.1:5000/get_client_token/123", timeout=3)
        .json()
        .get("token", "")
    )
    headers: Optional[Mapping[str, Union[str, bytes]]] = {
        "Content-Type": "application/json",
        "x-access-tokens": client_token,
    }

    return requests.request(
        "GET",
        f"http://127.0.0.1:5000/check_user_email/{email}",
        headers=headers,
        timeout=3,
    ).json()
