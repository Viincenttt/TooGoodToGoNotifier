from api.client import ApiClient

from config import AppConfiguration

def main():
    app_config = AppConfiguration()

    client = ApiClient()
    result = client.authenticate_by_email(app_config.email)
    print(result.polling_id)
    #polling_id = 'y'
    #polling_result = client.authenticate_by_polling_id('x', polling_id)
    #print(polling_result.access_token)

if __name__ == '__main__':
    main()