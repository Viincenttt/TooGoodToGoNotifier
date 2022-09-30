from api.client import ApiClient
import logging
import random
import time

from authentication.authenticator import Authenticator

class FavoritesScanner:
    def __init__(self, email: str, client: ApiClient) -> None:
        self.email = email
        self.client = client
        self.authenticator = Authenticator(self.client)

        self.time_between_scanning_in_seconds_from = 60
        self.time_between_scanning_in_seconds_to = 300

    def scan(self) -> None:
        while (True):
            self.scan_favorites()

            time_to_sleep = random.randint(self.time_between_scanning_in_seconds_from, self.time_between_scanning_in_seconds_to)
            logging.info(f"Scanning complete, sleeping for {time_to_sleep} seconds")
            time.sleep(time_to_sleep)

    def scan_favorites(self) -> None:
        access_token = self.authenticator.get_access_token(self.email)
        user_id = self.authenticator.user_id

        items = self.client.get_favorites_basket(access_token, user_id)
        for item in items:
            print(f"Id={item.item_id} Name={item.display_name} Available={item.items_available}")