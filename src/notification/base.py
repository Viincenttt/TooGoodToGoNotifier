from abc import ABC, abstractmethod

from api.models import GetFavoritesBasketItemResponse

class BaseNotification(ABC):
    @abstractmethod
    def notify(self, item: GetFavoritesBasketItemResponse) -> None:
        pass 