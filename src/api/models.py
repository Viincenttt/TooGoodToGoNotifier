class AuthenticateByEmailResponse:
    def __init__(self, state: str, polling_id: str):
        # {"state":"WAIT","polling_id":"55141f8e-7bf8-4503-97d2-c5c01eceaa33"}'
        self.state = state
        self.polling_id = polling_id

class UserResponse:
    def __init__(self, user_id: int):
        self.user_id = user_id

class StartupDataResponse:
    def __init__(self, user):
        self.user = UserResponse(**user)

class AuthenticateByPollingIdResponse:
    def __init__(self, access_token: str, refresh_token: str, startup_data):
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.startup_data = StartupDataResponse(**startup_data)