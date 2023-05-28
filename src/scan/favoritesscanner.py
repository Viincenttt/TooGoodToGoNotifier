from typing import Iterable
from api.client import ApiClient
import logging
import random
import time
from api.errors import TooGoodToGoApiError
from api.models import GetFavoritesBasketItemResponse
import datetime
import pytz

from authentication.authenticator import Authenticator
from notification.base import BaseNotification

class FavoritesScanner:
    def __init__(self, email: str, notifiers: Iterable[BaseNotification]) -> None:
        self.email = email
        self.client = ApiClient()
        self.authenticator = Authenticator(self.client)
        self.previous_favorites_scan_result = {}
        self.notifiers = notifiers

        self.time_between_scanning_in_seconds_from = 30
        self.time_between_scanning_in_seconds_to = 120

    def scan_continuously(self) -> None:
        while (True):
            if (self.__is_within_time_to_scan()):
                logging.info('Start scanning favorites')
                self.scan_favorites()
            else:
                logging.info('Not scanning because we dont expect any new items during these times')

            time_to_sleep = random.randint(self.time_between_scanning_in_seconds_from, self.time_between_scanning_in_seconds_to)
            logging.info(f"Scanning complete, sleeping for {time_to_sleep} seconds")
            time.sleep(time_to_sleep)
            

    def scan_favorites(self) -> None:
        try:
            access_token = self.authenticator.get_access_token(self.email)
            user_id = self.authenticator.user_id

            items = self.client.get_favorites_basket(access_token, user_id)
            for item in items:
                logging.info(f'Favorite item status: Store={item.display_name} Items Available={item.items_available}',
                    extra={'custom_dimensions': {'store': item.display_name, 'items_available': item.items_available }})

                if self.__is_item_newly_available(item):
                    self.__notify_new_item_available(item)

                self.previous_favorites_scan_result[item.item_id] = item.items_available
        except TooGoodToGoApiError as api_err:
            logging.exception(api_err, exc_info=True)
            if api_err.status_code == 401:                
                logging.warning("401 status code retrieved, refreshing access token")
                self.__refresh_token()
            
        except Exception as err:
            logging.exception(err, exc_info=True)

    def __is_within_time_to_scan(self) -> None:
        ams_timezone = pytz.timezone('Europe/Amsterdam')
        now = datetime.datetime.now(ams_timezone)
        return now.hour >= 7 and now.hour <= 22

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
        for notifier in self.notifiers:
            # Wrap in try catch, so that if one notification system fails, the next ones are still executed
            try:
                notifier.notify(item)
            except Exception as err:
                logging.exception(err, exc_info=True)

    def __refresh_token(self) -> None:
        try:
            self.authenticator.refresh_access_token()
        except Exception as err:
            logging.exception("Error while refreshing token", err, exc_info=True)