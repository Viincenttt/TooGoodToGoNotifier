from http import HTTPStatus
import json
from typing import Any, Dict, List
import requests
import logging

from api.errors import TooGoodToGoApiError, TooGoodToGoRateLimitError
from api.models import AuthenticateByEmailResponse, AuthenticateByPollingIdResponse, GetFavoritesBasketItemResponse, RefreshAccessTokenResponse

class ApiClient:
    BASE_URI = "https://apptoogoodtogo.com/api"

    def __init__(self):
        logging.getLogger("urllib3").setLevel(logging.WARNING)

        self.session = requests.Session()

        self._headers = {
            "user-agent": "TGTG/23.7.12 Dalvik/2.1.0 (Linux; U; Android 9; AFTKA Build/PS7285.2877N",
            "accept-language": "en-UK",
            "accept": "application/json",
            "content-type": "application/json; charset=utf-8",
            "Accept-Encoding": "gzip"
        }

    def get_favorites_basket(self, access_token: str, user_id: int) -> List[GetFavoritesBasketItemResponse]:
        uri = f"{self.BASE_URI}/item/v8/"
        body = {
            "user_id": user_id,
            "origin": {"longitude": 0.0, "latitude": 0.0},
            "radius": 1,
            "page_size": 400,
            "page": 1,            
            "discover": False,
            "favorites_only": True,
            "item_categories": [],
            "diet_categories": [],
            "pickup_earliest": None,
            "pickup_latest": None,
            "search_phrase": None,
            "with_stock_only": False,
            "hidden_only": False,
            "we_care_only": False,
        }
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        response = self._post(uri, body, headers)

        result = []
        for item in response["items"]:
            itemResponse = GetFavoritesBasketItemResponse(
                item["item"]["item_id"],
                item["display_name"],
                item["items_available"]
            )
            result.append(itemResponse)

        return result        

    def authenticate_by_email(self, email: str) -> AuthenticateByEmailResponse:
        uri = f"{self.BASE_URI}/auth/v3/authByEmail"
        body = {
            "device_type": "ANDROID",
            "email": email
        }

        response = self._post(uri, body)
        return AuthenticateByEmailResponse(
            response["polling_id"]
        )

    def authenticate_by_polling_id(self, email: str, polling_id: str) -> AuthenticateByPollingIdResponse:
        uri = f"{self.BASE_URI}/auth/v3/authByRequestPollingId"
        body = {
            "device_type": "ANDROID",
            "email": email,
            "request_polling_id": polling_id
        }

        response = self._post(uri, body)
        return AuthenticateByPollingIdResponse(
            response["access_token"], 
            response["refresh_token"],
            response["access_token_ttl_seconds"],
            response["startup_data"]["user"]["user_id"]
        )

    def refresh_access_token(self, refresh_token: str) -> RefreshAccessTokenResponse:
        uri = f"{self.BASE_URI}/auth/v3/token/refresh"
        body = {
            "refresh_token": refresh_token
        }

        response = self._post(uri, body)
        return RefreshAccessTokenResponse(
            response["access_token"], 
            response["refresh_token"],
            response["access_token_ttl_seconds"]
        )

    def _post(self, uri: str, body, headers = None) -> Any:
        if (headers is not None):
            headers.update(self._headers)
        else:
            headers = self._headers

        self.session.headers = headers
        logging.debug(f"Sending request to Uri={uri} RequestBody={body} Method=POST",
            extra={'custom_dimensions': {'uri': uri, 'request_body': body, 'method': 'POST' }})

        response = self.session.post(uri, json=body)

        logging.debug(f"Received response from Uri={uri} Response={response.content} Method=POST",
            extra={'custom_dimensions': {'uri': uri, 'response_body': response.content, 'method': 'POST' }})

        if response.status_code in (HTTPStatus.OK, HTTPStatus.ACCEPTED):
            try:
                result = response.json()
                return result
            except ValueError as err:
                raise TooGoodToGoApiError(response.status_code, response.content)
        
        if (response.status_code == HTTPStatus.TOO_MANY_REQUESTS):
            raise TooGoodToGoRateLimitError(response.status_code, response.content)

        raise TooGoodToGoApiError(response.status_code, response.content)

