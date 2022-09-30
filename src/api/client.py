from http import HTTPStatus
import json
from typing import Any, Dict
import requests

from api.errors import TooGoodToGoApiError
from api.models import AuthenticateByEmailResponse, AuthenticateByPollingIdResponse

class ApiClient:
    BASE_URI = "https://apptoogoodtogo.com/api"

    def __init__(self):
        self._headers = {
            "user-agent": "TGTG/{} Dalvik/2.1.0 (Linux; U; Android 10; SM-G935F Build/NRD90M)",
            "accept-language": "en-UK",
            "Accept-Encoding": "gzip",
            "Content-Type": "application/json; charset=utf8"
        }

    def authenticate_by_email(self, email: str) -> AuthenticateByEmailResponse:
        uri = f"{self.BASE_URI}/auth/v3/authByEmail"
        body = {
            "device_type": "ANDROID",
            "email": email
        }

        response = self._post(uri, body)
        return AuthenticateByEmailResponse(response["polling_id"])

    def authenticate_by_polling_id(self, email: str, polling_id: str) -> AuthenticateByPollingIdResponse:
        uri = f"{self.BASE_URI}/auth/v3/authByRequestPollingId"
        body = {
            "device_type": "ANDROID",
            "email": email,
            "request_polling_id": polling_id
        }

        response = self._post(uri, body)
        return AuthenticateByPollingIdResponse(response["access_token"], response["refresh_token"])

    def _post(self, uri: str, body: Dict) -> Any:
        response = requests.post(uri, json.dumps(body), headers=self._headers)

        if response.status_code in (HTTPStatus.OK, HTTPStatus.ACCEPTED):
            try:
                result = response.json()
                return result
            except ValueError as err:
                raise TooGoodToGoApiError(response.status_code, response.content)
        
        raise TooGoodToGoApiError(response.status_code, response.content)

