from api.client import ApiClient

def main():
    client = ApiClient()
    #result = client.authenticate_by_email('x')
    polling_id = 'y'
    polling_result = client.authenticate_by_polling_id('x', polling_id)
    print(polling_result.access_token)

if __name__ == '__main__':
    main()