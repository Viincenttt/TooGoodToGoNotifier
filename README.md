# To Good To Go Notifier

## Introduction

### Disclaimer
This project is in no way affiliated with Too Good To Go. Use TooGoodToGoNotifier at your own risk. Using TooGoodToGoNotifier may violate the Too Good To Go user agreement.

### What is Too Good To Go?
[Too Good To Go](https://toogoodtogo.com/en-us) fights food waste through their app, that connects users with stores and restaurants that have unsold surplus food at the end of the day. Users of the Too Good To Go app can get bags of surplus stock that is either close to the end of its shelf life or on the final day of its “best before/use by” date. These bags are packaged together at random but the price is a fraction of the full retail value.

### What does the TooGoodToGoNotifier application do?
The official Too Good To Go app does not have store specific notifications when surplus food is available. This means that users continually have to refresh the app so they don't miss any availability from their favorite stores. The TooGoodToGoNotifier solves this problem by sending you notifications whenever one of your favorites stores has new availability. This way you'll never miss another bag of food from your favorite store again!

## How to use
### Installing requirements
The requirements are listed in the `src/requirements.txt` file. To install them, simply run:
```
cd src
pip install -r requirements.txt
```

### Enter your settings
Enter your settings in the `src/.env` file:
```
EMAIL=YOUR_TOO_GOOD_TO_GO_EMAIL
LOGGING_LEVEL=INFO
AZURE_APP_INSIGHTS_CONNECTION_STR=YOUR_APP_INSIGHTS_CONNECTION_STR
SENDGRID_API_KEY=YOUR_SENDGRID_API_KEY
SENDGRID_FROM_EMAIL=YOUR_SENDGRID_FROM_EMAIL
SENDGRID_TO_EMAIL=YOUR_SENDGRID_TO_EMAIL
```

### Notification types
Two types of notifications are supported: Log notifications and SendGrid notifications. 

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

### Configuring notifications
By default, both the log notifications and the SendGrid notifications are enabled. In the `src/__main__.py` file you can setup which notifications it should use. 
```
scanner = FavoritesScanner(
  email=app_config.email,
  notifiers=[
    LogNotifier(),
    SendgridNotifier(
      api_key=app_config.sendgrid_api_key,
      from_email=app_config.sendgrid_from_email,
      to_emails=app_config.sendgrid_to_email
    )
  ]
)
```
