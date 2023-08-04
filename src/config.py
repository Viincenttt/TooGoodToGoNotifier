from dotenv import load_dotenv
import os
from os.path import join, dirname

class AppConfiguration:
    def __init__(self):
        load_dotenv(join(dirname(__file__), '.env'))
        load_dotenv(join(dirname(__file__), '.development.env'), override=True)

        self.email = os.environ.get('EMAIL')
        self.logging_level = os.environ.get('LOGGING_LEVEL')
        self.azure_app_insights_connection_str = os.environ.get('AZURE_APP_INSIGHTS_CONNECTION_STR')
        self.sendgrid_api_key = os.environ.get('SENDGRID_API_KEY')
        self.sendgrid_from_email = os.environ.get('SENDGRID_FROM_EMAIL')
        self.sendgrid_to_email = os.environ.get('SENDGRID_TO_EMAIL')
        self.telegram_bot_token = os.environ.get('TELEGRAM_BOT_TOKEN')
        self.telegram_chat_id = os.environ.get('TELEGRAM_CHAT_ID')