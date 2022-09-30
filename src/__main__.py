from api.client import ApiClient
from authentication.authenticator import Authenticator

from config import AppConfiguration
import logging

from scan.favoritesscanner import FavoritesScanner

def main():
    app_config = AppConfiguration()
    logging_level = getattr(logging, app_config.logging_level.upper(), None)
    logging.basicConfig(level=logging_level)
    
    scanner = FavoritesScanner(app_config.email)
    scanner.scan_continuously()

if __name__ == '__main__':
    main()