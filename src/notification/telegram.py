import requests

from api.models import GetFavoritesBasketItemResponse

class TelegramClient:
    BASE_URI = "https://api.telegram.org"

    def __init__(self, bot_token: str) -> None:
        self.bot_token = bot_token

    def send_message(self, chat_id: str, message: str):
        url = f"{self.BASE_URI}/bot{self.bot_token}/sendMessage?chat_id={chat_id}&text={message}"
        response = requests.get(url=url)
        response.raise_for_status()


class TelegramNotifier:
    def __init__(self, telegram_client: TelegramClient, chat_id: str) -> None:
        self.chat_id = chat_id
        self.telegram_client = telegram_client

    def notify(self, item: GetFavoritesBasketItemResponse) -> None:
        message = f'New availability for Store={item.display_name} - Number of available items={item.items_available}'
        self.telegram_client.send_message(self.chat_id, message=message)

