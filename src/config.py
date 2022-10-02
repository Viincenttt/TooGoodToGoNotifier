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