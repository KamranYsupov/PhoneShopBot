import requests


def verify_status_code(
    response: requests.Response,
    expected_status_code: int = 200,
) -> requests.Response.text:
    if response.status_code != expected_status_code:
        raise ValueError(response.text)
    else:
        return response.text