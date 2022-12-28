from opencensus.ext.azure.log_exporter import AzureLogHandler

from config import AppConfiguration
import logging
from logging.handlers import RotatingFileHandler
from notification.log import LogNotifier
from notification.email import SendgridNotifier
from notification.telegram import TelegramClient, TelegramNotifier

from scan.favoritesscanner import FavoritesScanner

def initializeLogging(app_config: AppConfiguration) -> None:
    logging_level = getattr(logging, app_config.logging_level.upper(), None)
    
    logging.basicConfig(
        format='%(asctime)s %(levelname)-8s %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        level=logging_level,
        handlers=[
            AzureLogHandler(connection_string=app_config.azure_app_insights_connection_str),
            RotatingFileHandler('debug.log', maxBytes=100000, backupCount=10),
            logging.StreamHandler()
        ]
    )

def main():
    app_config = AppConfiguration()
    initializeLogging(app_config)

    scanner = FavoritesScanner(
        email=app_config.email,
        notifiers=[
            LogNotifier(),
            TelegramNotifier(
                telegram_client=TelegramClient(app_config.telegram_bot_token),
                chat_id=app_config.telegram_chat_id
            )
        ]
    )
    scanner.scan_continuously()    

if __name__ == '__main__':
    main()