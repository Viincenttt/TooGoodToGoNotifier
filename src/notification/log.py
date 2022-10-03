from api.models import GetFavoritesBasketItemResponse
import logging

from notification.base import BaseNotification

class LogNotifier(BaseNotification):
    def notify(self, item: GetFavoritesBasketItemResponse) -> None:
        logging.info(f'New favorite item available in Good To Go - Store={item.display_name} Items Available={item.items_available}',
            extra={'custom_dimensions': {'store_status_changed': True, 'store': item.display_name, 'items_available': item.items_available }})