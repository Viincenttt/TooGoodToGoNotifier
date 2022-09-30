import unittest
from unittest.mock import MagicMock, Mock, patch
from api.client import ApiClient
from api.models import GetFavoritesBasketItemResponse
from authentication.authenticator import Authenticator

from scan.favoritesscanner import FavoritesScanner

class TestFavoritesScanner(unittest.TestCase):
    def test_no_items_available(self):
        # Arrange
        email = 'test@email.com'
        scanner = FavoritesScanner(email)

        authenticator_mock = Mock()
        authenticator_mock.get_access_token.return_value = 'test_access_token'
        authenticator_mock.user_id = 'test_user_id'

        api_client_mock = Mock()
        api_client_mock.get_favorites_basket.return_value = [
            GetFavoritesBasketItemResponse('item-id-1', 'store-1', 0),
            GetFavoritesBasketItemResponse('item-id-2', 'store-2', 0),
        ]

        scanner.authenticator = authenticator_mock
        scanner.client = api_client_mock

        # Act
        with self.assertLogs(level='INFO') as log:
            scanner.scan_favorites()

            # Assert
            self.assertIn('INFO:root:Favorite item status: Store=store-1 Items Available=0', log.output[0])
            self.assertIn('INFO:root:Favorite item status: Store=store-2 Items Available=0', log.output[1])
            self.assertEqual(len(log.output), 2)

        
        authenticator_mock.get_access_token.assert_called_once_with(email)
        api_client_mock.get_favorites_basket.assert_called_once_with(authenticator_mock.get_access_token.return_value, authenticator_mock.user_id)        

if __name__ == '__main__':
    unittest.main()

