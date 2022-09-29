from api.client import ApiClient

def main():
    client = ApiClient()
    result = client.authenticate_by_email('x')
    print(result.polling_id)

if __name__ == '__main__':
    main()