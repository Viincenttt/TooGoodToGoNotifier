from api.client import ApiClient
from authentication.authenticator import Authenticator
from opencensus.ext.azure.log_exporter import AzureLogHandler

from config import AppConfiguration
import logging
from logging.handlers import RotatingFileHandler

from scan.favoritesscanner import FavoritesScanner

def initializeLogging(app_config: AppConfiguration) -> None:
    logging_level = getattr(logging, app_config.logging_level.upper(), None)
    
    logging.basicConfig(
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
    
    scanner = FavoritesScanner(app_config.email)
    scanner.scan_continuously()

if __name__ == '__main__':
    main()