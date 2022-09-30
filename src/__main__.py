from api.client import ApiClient
from authentication.authenticator import Authenticator

from config import AppConfiguration
import logging

from scan.favoritesscanner import FavoritesScanner

def main():
    logging.basicConfig(level=logging.DEBUG)
    app_config = AppConfiguration()

    client = ApiClient()
    scanner = FavoritesScanner(app_config.email, client)
    scanner.scan_continuously()

if __name__ == '__main__':
    main()