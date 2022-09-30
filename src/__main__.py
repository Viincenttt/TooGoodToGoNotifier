from api.client import ApiClient
from authentication.authenticator import Authenticator

from config import AppConfiguration
import logging

def main():
    logging.basicConfig(level=logging.DEBUG)
    app_config = AppConfiguration()

    client = ApiClient()
    authenticator = Authenticator(client)
    result = authenticator.login(app_config.email)
    
    print(result.access_token)
    #polling_id = 'y'
    #polling_result = client.authenticate_by_polling_id('x', polling_id)
    #print(polling_result.access_token)

if __name__ == '__main__':
    main()