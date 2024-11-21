from typing import Any



class CleanResponse:
    def __init__(self, response: Any) :
        self._response = response

    def location(self) -> str:
        full_location = self._response.headers['Location']
        without_protocol = full_location.split("//")[1]
        without_localhost = without_protocol.split("/", 1)[1]
        return "/" + without_localhost

BASE_URL = "/any_user/todo"
