import base64
from typing import Any



class CleanResponse:
    def __init__(self, response: Any) :
        self._response = response

    def location(self) -> str:
        full_location = self._response.headers['Location']
        without_protocol = full_location.split("//")[1]
        without_localhost = without_protocol.split("/", 1)[1]
        return "/" + without_localhost

BASE_URL = "/todo"


def header_with_good_authentication():
    auth = base64.b64encode(b"test@mail.fr:test@mail.fr").decode('utf-8')
    headers = {"Authorization": f"Basic {auth}"}
    return headers
