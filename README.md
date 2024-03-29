# Too Good To Go Notifier

## Introduction

### Disclaimer
This project is in no way affiliated with Too Good To Go. Use TooGoodToGoNotifier at your own risk. Using TooGoodToGoNotifier may violate the Too Good To Go user agreement.

### What is Too Good To Go?
[Too Good To Go](https://toogoodtogo.com/en-us) fights food waste through their app, that connects users with stores and restaurants that have unsold surplus food at the end of the day. Users of the Too Good To Go app can get bags of surplus stock that is either close to the end of its shelf life or on the final day of its “best before/use by” date. These bags are packaged together at random but the price is a fraction of the full retail value.

### What does the TooGoodToGoNotifier application do?
The official Too Good To Go app does not have store specific notifications when surplus food is available. This means that users continually have to refresh the app so they don't miss any availability from their favorite stores. The TooGoodToGoNotifier solves this problem by sending you notifications whenever one of your favorites stores has new availability. This way you'll never miss another bag of food from your favorite store again!

## How to use
### Enter your settings
Enter your settings in the `src/.env` file:
```
EMAIL=YOUR_TOO_GOOD_TO_GO_EMAIL
LOGGING_LEVEL=INFO
AZURE_APP_INSIGHTS_CONNECTION_STR=YOUR_APP_INSIGHTS_CONNECTION_STR
SENDGRID_API_KEY=YOUR_SENDGRID_API_KEY
SENDGRID_FROM_EMAIL=YOUR_SENDGRID_FROM_EMAIL
SENDGRID_TO_EMAIL=YOUR_SENDGRID_TO_EMAIL
TELEGRAM_BOT_TOKEN=YOUR_TELEGRAM_BOT_TOKEN
TELEGRAM_CHAT_ID=YOUR_TELEGRAM_CHAT_ID
```

### With Docker
Build the image:
```
docker build -t toogoodtogo-notifier .
```

Enter your settings in the `/src/.env` file and run the following command:
```
docker run --env-file src/.env toogoodtogo-notifier
```

### Without Docker
#### Installing requirements
The requirements are listed in the `src/requirements.txt` file. To install them, simply run:
```
pip install -r requirements.txt
cd src
python __main__.py
```

### Successful start-up
A successful startup will show the following output:
```
2023-08-04 10:02:07 INFO     Start scanning favorites
2023-08-04 10:02:07 INFO     Authentication not available yet, trying again in 17 seconds
```

Too Good To Go uses passwordless authentication. That means that whenever you start up TooGoodToGoNotifier for the first time, you'll receive an e-mail from Too Good To Go to verify a new login. Since TooGoodToGoNotifier caches the refresh token, you won't have to authenticate again the next time you start the TooGoodToGoNotifier application. 

### Notification types
Three types of notifications are supported: Log notifications, SendGrid notifications and Telegram notifications.

#### Log notifications
Log notifications allow you to log to Application Insights. Inside Application Insights, you can setup alerts and action groups to notify you whenever a store has new available stock. The Application Insights query you could use for the alert is:
```
union traces
| where cloud_RoleName == "__main__.py"
| where customDimensions.store_status_changed == true
| order by timestamp
```

#### Sendgrid notifications
With [SendGrid](https://sendgrid.com/) you can setup e-mail notifications. Whenever one of your favorite stores has new availability, you'll receive an e-mail that specificies which store has availability and how much availability it has. 

#### Telegram notifications
The TooGoodToGoNotifier can also send Telegram notifications. In order for this to work, you'll have to create a bot token and setup a chat id to which the TooGoodToGoNotifier app will send the messages to. More information can be found [here](https://medium.com/codex/using-python-to-send-telegram-messages-in-3-simple-steps-419a8b5e5e2). Once you have the bot token and chat id, simply add them to the .env file settings.

#### Configuring notifications
By default, both the log notifications and the Telegram notifications are enabled. In the `src/__main__.py` file you can setup which notifications it should use. 
```python
scanner = FavoritesScanner(
  email=app_config.email,
  notifiers=[
    LogNotifier(),
    TelegramNotifier(
        telegram_client=TelegramClient(app_config.telegram_bot_token),
        chat_id=app_config.telegram_chat_id
    )
  ]
)
```

Alternatively, you could setup the SendgridNotifier by simply adding the SendgridNotifier class to the notifiers array:
```
notifiers=[
    SendgridNotifier(
        api_key=app_config.sendgrid_api_key,
        from_email=app_config.sendgrid_from_email,
        to_emails=app_config.sendgrid_to_email
    )
]
```

#### Adding custom notifiers
Adding custom notifiers is incredibly easy. Add your own custom notifier to the `notifiers` property of the `FavoritesScanner`. Your own notifier has to extend the abstract `BaseNotification` class. For example:

*customnotification.py:*
```python
class CustomNotifier(BaseNotification):
    def notify(self, item: GetFavoritesBasketItemResponse) -> None:
        # Your custom notification logic here
```
*__main__.py:*
```python
scanner = FavoritesScanner(
  email=app_config.email,
  notifiers=[
    CustomNotifier()
  ]
)
```

The `notify` method of your `CustomNotifier` will now be called whenever one of your favorite Too Good To Go stores has new availability!

