from asyncio.log import logger
import random
from api.client import ApiClient
from api.errors import TooGoodToGoApiError
from authentication.errors import TooGoodToGoLoginPollingError
import time
import logging
from datetime import datetime, timedelta

class Authenticator:
    def __init__(self, client: ApiClient):
        self.client = client

        self.max_polling_tries = 10
        self.time_between_polling_in_seconds_from = 10
        self.time_between_polling_in_seconds_to = 30

        self.access_token = None
        self.refresh_token = None
        self.access_token_valid_until = None   

    def get_access_token(self, email: str):
        if self.access_token is not None:                        
            if (self.__should_refresh_access_token):
                refresh_token_result = self.client.refresh_access_token(self.refresh_token)
                self.access_token = refresh_token_result.access_token
                self.refresh_token = refresh_token_result.refresh_token
                self.access_token_valid_until = datetime.now() + timedelta(seconds=refresh_token_result.access_token_ttl_seconds)            

            return self.access_token        

        # TODO: Cache access_token in file / settings, so we can load it in app startup

        login_result = self.login(email)
        self.access_token = login_result.access_token
        self.refresh_token = login_result.refresh_token
        self.access_token_valid_until = datetime.now() + timedelta(seconds=login_result.access_token_ttl_seconds)

    def login(self, email: str):
        polling_id = self.__get_polling_id(email)

        for _ in range(self.max_polling_tries):
            authentication_result = self.__authenticate_with_polling_id(email, polling_id)
            if authentication_result is not None:
                logging.info("Successfully retrieved authentication token and refresh token")
                return authentication_result
            else:
                time_to_sleep = random.randint(self.time_between_polling_in_seconds_from, self.time_between_polling_in_seconds_to)
                logging.info(f"Authentication not available yet, trying again in {time_to_sleep} seconds")
                time.sleep(time_to_sleep)

        raise TooGoodToGoLoginPollingError(f'Max polling retries reached MaxRetries={self.max_polling_tries}')

    def __get_polling_id(self, email: str): 
        result = self.client.authenticate_by_email(email)
        return result.polling_id

    def __authenticate_with_polling_id(self, email:str, polling_id: str):
        try:
            result = self.client.authenticate_by_polling_id(email, polling_id)
            return result
        except TooGoodToGoApiError as err:
            return None    

    def __should_refresh_access_token(self):
        current_time = datetime.now()
        time_to_refresh_access_token = self.access_token_valid_until - timedelta(seconds=600)

        return current_time >= time_to_refresh_access_token