from api.client import ApiClient
import logging
import random
import time
from api.models import GetFavoritesBasketItemResponse

from authentication.authenticator import Authenticator

class FavoritesScanner:
    def __init__(self, email: str) -> None:
        self.email = email
        self.client = ApiClient()
        self.authenticator = Authenticator(self.client)
        self.previous_favorites_scan_result = {}

        self.time_between_scanning_in_seconds_from = 60
        self.time_between_scanning_in_seconds_to = 300

    def scan_continuously(self) -> None:
        while (True):
            self.scan_favorites()

            time_to_sleep = random.randint(self.time_between_scanning_in_seconds_from, self.time_between_scanning_in_seconds_to)
            logging.info(f"Scanning complete, sleeping for {time_to_sleep} seconds")
            time.sleep(time_to_sleep)

    def scan_favorites(self) -> None:
        try:
            access_token = self.authenticator.get_access_token(self.email)
            user_id = self.authenticator.user_id

            items = self.client.get_favorites_basket(access_token, user_id)
            for item in items:
                logging.info(f'Favorite item status: Store={item.display_name} Items Available={item.items_available}')

                if self.__is_item_newly_available(item):
                    self.__notify_new_item_available(item)

                self.previous_favorites_scan_result[item.item_id] = item.items_available
        except Exception as err:
            logging.exception(err, exc_info=True)

    def __is_item_newly_available(self, item: GetFavoritesBasketItemResponse) -> bool:
        if item.items_available == 0:
            return False

        is_item_in_previous_scan = item.item_id in self.previous_favorites_scan_result
        if is_item_in_previous_scan:
            # Item was in previous scan. If it wasn't available in previous run, but is available now, return true
            return self.previous_favorites_scan_result[item.item_id] == 0
        else:
            # Item has availability, but was not in previous scan (new favorite item or first run)
            return True

    def __notify_new_item_available(self, item: GetFavoritesBasketItemResponse) -> None:
        logging.info(f'New favorite item available in Good To Go - Store={item.display_name} Items Available={item.items_available}')