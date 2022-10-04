from api.models import GetFavoritesBasketItemResponse
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from notification.base import BaseNotification

class SendgridNotifier(BaseNotification):
    def __init__(self, api_key: str, from_email: str, to_emails: str) -> None:
        self.api_key = api_key
        self.from_email = from_email
        self.to_emails = to_emails.split(';')

    def notify(self, item: GetFavoritesBasketItemResponse) -> None:
        subject = '2Good2Go notification'
        body = f'New availability for Store={item.display_name} - Number of available items={item.items_available}'

        message = Mail(
            from_email=self.from_email,
            to_emails=self.to_emails,
            subject=subject,
            html_content=body)

        sg = SendGridAPIClient(self.api_key)
        sg.send(message)