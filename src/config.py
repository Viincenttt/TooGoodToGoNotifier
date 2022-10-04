from dotenv import dotenv_values

class AppConfiguration:
    def __init__(self):
        config = {
            **dotenv_values(".env"), 
            **dotenv_values(".development.env")
        }

        self.email = config['EMAIL']
        self.logging_level = config['LOGGING_LEVEL']
        self.azure_app_insights_connection_str = config['AZURE_APP_INSIGHTS_CONNECTION_STR']
        self.sendgrid_api_key = config['SENDGRID_API_KEY']
        self.sendgrid_from_email = config['SENDGRID_FROM_EMAIL']
        self.sendgrid_to_email = config['SENDGRID_TO_EMAIL']