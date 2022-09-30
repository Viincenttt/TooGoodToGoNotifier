class AuthenticateByEmailResponse:
    def __init__(self, polling_id: str):
        # {"state":"WAIT","polling_id":"55141f8e-7bf8-4503-97d2-c5c01eceaa33"}'
        self.polling_id = polling_id

class AuthenticateByPollingIdResponse:
    def __init__(self, access_token: str, refresh_token: str, access_token_ttl_seconds: int):
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.access_token_ttl_seconds = access_token_ttl_seconds

class RefreshAccessTokenResponse:
    def __init__(self, access_token: str, refresh_token: str, access_token_ttl_seconds: int):
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.access_token_ttl_seconds = access_token_ttl_seconds