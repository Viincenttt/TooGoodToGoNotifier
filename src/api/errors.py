class TooGoodToGoApiError(Exception):
    pass

class TooGoodToGoRateLimitError(TooGoodToGoApiError):
    pass