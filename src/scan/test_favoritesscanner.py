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

        scanner.authenticator = self.__create_authenticator_mock()
        scanner.client = self.__create_api_client_mock(0)

        # Act
        with self.assertLogs(level='INFO') as log:
            scanner.scan_favorites()

            # Assert
            self.assertIn('INFO:root:Favorite item status: Store=store-1 Items Available=0', log.output[0])
            self.assertIn('INFO:root:Favorite item status: Store=store-2 Items Available=0', log.output[1])
            self.assertEqual(len(log.output), 2)
        
        scanner.authenticator.get_access_token.assert_called_once_with(email)
        scanner.client.get_favorites_basket.assert_called_once_with(
            scanner.authenticator.get_access_token.return_value, 
            scanner.authenticator.user_id)

    def test_item_available(self):
        # Arrange
        email = 'test@email.com'
        available_items = 1
        scanner = FavoritesScanner(email)        

        scanner.authenticator = self.__create_authenticator_mock()
        scanner.client = self.__create_api_client_mock(available_items)

        # Act
        with self.assertLogs(level='INFO') as log:
            scanner.scan_favorites()

            # Assert
            self.assertIn('INFO:root:Favorite item status: Store=store-1 Items Available=0', log.output[0])
            self.assertIn(f'INFO:root:Favorite item status: Store=store-2 Items Available={available_items}', log.output[1])
            self.assertIn(f'INFO:root:New favorite item available in Good To Go - Store=store-2 Items Available={available_items}', log.output[2])
            self.assertEqual(len(log.output), 3)
        
        scanner.authenticator.get_access_token.assert_called_once_with(email)
        scanner.client.get_favorites_basket.assert_called_once_with(
            scanner.authenticator.get_access_token.return_value, 
            scanner.authenticator.user_id)

    def __create_authenticator_mock(self) -> Mock:
        authenticator_mock = Mock()
        authenticator_mock.get_access_token.return_value = 'test_access_token'
        authenticator_mock.user_id = 'test_user_id'

        return authenticator_mock

    def __create_api_client_mock(self, available_items: int) -> Mock:
        api_client_mock = Mock()
        api_client_mock.get_favorites_basket.return_value = [
            GetFavoritesBasketItemResponse('item-id-1', 'store-1', 0),
            GetFavoritesBasketItemResponse('item-id-2', 'store-2', available_items),
        ]

        return api_client_mock

if __name__ == '__main__':
    unittest.main()

