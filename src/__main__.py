from opencensus.ext.azure.log_exporter import AzureLogHandler

from config import AppConfiguration
import logging
from logging.handlers import RotatingFileHandler
from notification.log import LogNotifier
from notification.email import SendgridNotifier

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
            SendgridNotifier(
                api_key=app_config.sendgrid_api_key,
                from_email=app_config.sendgrid_from_email,
                to_emails=app_config.sendgrid_to_email
            )
        ]
    )
    scanner.scan_continuously()

if __name__ == '__main__':
    main()