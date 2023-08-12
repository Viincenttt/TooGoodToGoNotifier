using './container-instance.bicep'

param tgtgEmail = '<your-email>'
param sendGridApiKey = '<sendgrid-api-key>'
param sendGridFromEmail = '<sendgrid-from-email>'
param sendGridToEmail = '<sendgrid-to-email>'
param telegramBotToken = '<telegram-bot-token>'
param telegramChatId = '<telegram-chat-id>'
param environmentType = 'prod'
param image = 'tgtgcontainerregistryprod.azurecr.io/tgtg/service:latest'

