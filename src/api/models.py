class AuthenticateByEmailResponse:
    def __init__(self, polling_id: str) -> None:
        self.polling_id = polling_id

class AuthenticateByPollingIdResponse:
    def __init__(self, access_token: str, refresh_token: str, access_token_ttl_seconds: int, user_id: int) -> None:
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.access_token_ttl_seconds = access_token_ttl_seconds
        self.user_id = user_id

class RefreshAccessTokenResponse:
    def __init__(self, access_token: str, refresh_token: str, access_token_ttl_seconds: int) -> None:
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.access_token_ttl_seconds = access_token_ttl_seconds

class GetFavoritesBasketItemResponse:
    def __init__(self, item_id: str, display_name: str, items_available: int) -> None:
        self.item_id = item_id
        self.display_name = display_name
        self.items_available = items_available