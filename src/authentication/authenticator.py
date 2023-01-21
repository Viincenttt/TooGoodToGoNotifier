from asyncio.log import logger
import random
from api.client import ApiClient
from api.errors import TooGoodToGoApiError
from authentication.errors import TooGoodToGoLoginPollingError
import time
import logging
from datetime import datetime, timedelta
import configparser

class Authenticator:
    CONFIG_FILE_NAME = 'authentication_cache.ini'
    CONFIG_AUTH_SECTION_NAME = 'TOKENS'
    CONFIG_AUTH_SECTION_ACCESS_TOKEN = 'AccessToken'
    CONFIG_AUTH_SECTION_REFRESH_TOKEN = 'RefreshToken'
    CONFIG_AUTH_SECTION_ACCESS_TOKEN_VALID_UNTIL = 'AccessTokenValidUntil'
    CONFIG_AUTH_SECTION_USER_ID = 'UserId'

    def __init__(self, client: ApiClient):
        self.client = client

        self.max_polling_tries = 10
        self.time_between_polling_in_seconds_from = 10
        self.time_between_polling_in_seconds_to = 30

        self.config = configparser.ConfigParser()
        self.config.read(self.CONFIG_FILE_NAME)

        self.access_token = self.config.get(self.CONFIG_AUTH_SECTION_NAME, self.CONFIG_AUTH_SECTION_ACCESS_TOKEN, fallback=None)
        self.refresh_token = self.config.get(self.CONFIG_AUTH_SECTION_NAME, self.CONFIG_AUTH_SECTION_REFRESH_TOKEN, fallback=None)
        
        user_id = self.config.get(self.CONFIG_AUTH_SECTION_NAME, self.CONFIG_AUTH_SECTION_USER_ID, fallback=None)
        if user_id is not None:
            self.user_id = int(user_id)

        access_token_valid_until = self.config.get(self.CONFIG_AUTH_SECTION_NAME, self.CONFIG_AUTH_SECTION_ACCESS_TOKEN_VALID_UNTIL, fallback=None)
        if access_token_valid_until is not None:
            self.access_token_valid_until = datetime.fromisoformat(access_token_valid_until)

    def get_access_token(self, email: str):
        if self.access_token is not None:                        
            if (self.__should_refresh_access_token()):
                self.refresh_access_token()

            return self.access_token

        login_result = self.__login(email)
        self.__set_authentication_tokens(
                    login_result.access_token, 
                    login_result.refresh_token, 
                    login_result.access_token_ttl_seconds,
                    login_result.user_id
        )

        return self.access_token

    def refresh_access_token(self):
        refresh_token_result = self.client.refresh_access_token(self.refresh_token)
        self.__set_authentication_tokens(
            refresh_token_result.access_token, 
            refresh_token_result.refresh_token, 
            refresh_token_result.access_token_ttl_seconds,
            self.user_id
        )

    def __login(self, email: str):
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

    def __set_authentication_tokens(self, access_token: str, refresh_token: str, access_token_ttl_seconds: int, user_id: int):
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.access_token_valid_until = datetime.now() + timedelta(seconds=access_token_ttl_seconds)
        self.user_id = user_id

        self.__save_authentication_tokens_to_file(self.access_token, self.refresh_token, self.access_token_valid_until, user_id)    

    def __save_authentication_tokens_to_file(self, access_token: str, refresh_token: str, access_token_valid_until: datetime, user_id: int):
        with open(self.CONFIG_FILE_NAME, 'w') as configfile:
            if (self.config.has_section(self.CONFIG_AUTH_SECTION_NAME) == False):
                self.config.add_section(self.CONFIG_AUTH_SECTION_NAME)

            self.config.set(self.CONFIG_AUTH_SECTION_NAME, self.CONFIG_AUTH_SECTION_ACCESS_TOKEN, access_token)
            self.config.set(self.CONFIG_AUTH_SECTION_NAME, self.CONFIG_AUTH_SECTION_REFRESH_TOKEN, refresh_token)
            self.config.set(self.CONFIG_AUTH_SECTION_NAME, self.CONFIG_AUTH_SECTION_ACCESS_TOKEN_VALID_UNTIL, access_token_valid_until.isoformat())
            self.config.set(self.CONFIG_AUTH_SECTION_NAME, self.CONFIG_AUTH_SECTION_USER_ID, str(user_id))

            self.config.write(configfile)