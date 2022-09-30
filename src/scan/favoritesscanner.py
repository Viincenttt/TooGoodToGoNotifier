from api.client import ApiClient
import logging
import random
import time

from authentication.authenticator import Authenticator

class FavoritesScanner:
    def __init__(self, email: str, client: ApiClient):
        self.email = email
        self.client = client
        self.authenticator = Authenticator(self.client)

        self.time_between_scanning_in_seconds_from = 60
        self.time_between_scanning_in_seconds_to = 300

    def scan(self):
        while (True):
            time_to_sleep = random.randint(self.time_between_scanning_in_seconds_from, self.time_between_scanning_in_seconds_to)
            logging.info(f"Scanning complete, sleeping for {time_to_sleep} seconds")
            time.sleep(time_to_sleep)