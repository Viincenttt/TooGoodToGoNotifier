param tgtgEmail string
param sendGridApiKey string = ''
param sendGridFromEmail string = ''
param sendGridToEmail string = ''
param telegramBotToken string = ''
param telegramChatId string = ''
param location string = resourceGroup().location
param environmentType string = 'prod'
param image string = 'tgtgcontainerregistryprod.azurecr.io/tgtg/service:latest'

var containerRegistryName = 'tgtgcontainerregistry${environmentType}'
var containerGroupName = 'tgtgcontainergroupname${environmentType}'
var applicationInsightsName = 'tgtginsights${environmentType}'

resource containerRegistry 'Microsoft.ContainerRegistry/registries@2022-12-01' existing = {
  name: containerRegistryName
} 

resource applicationInsights 'Microsoft.Insights/components@2020-02-02' = {
  name: applicationInsightsName
  location: location
  kind: 'web'
  properties: {
    Application_Type: 'web'
  }
} 

resource containerGroup 'Microsoft.ContainerInstance/containerGroups@2021-09-01' = {
  name: containerGroupName
  location: location
  properties: {
    containers: [
      {
        name: containerGroupName
        properties: {
          image: image
          environmentVariables: [
            {
              name: 'EMAIL'
              value: tgtgEmail
            }
            {
              name: 'LOGGING_LEVEL'
              value: 'INFO'
            }
            {
              name: 'AZURE_APP_INSIGHTS_CONNECTION_STR'
              secureValue: applicationInsights.properties.ConnectionString
            }
            {
              name: 'SENDGRID_API_KEY'
              secureValue: sendGridApiKey
            }
            {
              name: 'SENDGRID_FROM_EMAIL'
              value: sendGridFromEmail
            }
            {
              name: 'SENDGRID_TO_EMAIL'
              value: sendGridToEmail
            }
            {
              name: 'TELEGRAM_BOT_TOKEN'
              secureValue: telegramBotToken
            }
            {
              name: 'TELEGRAM_CHAT_ID'
              value: telegramChatId
            }
          ]
          resources: {
            requests: {
              cpu: 1
              memoryInGB: 2
            }
          }
        }
      }
    ]
    imageRegistryCredentials: [
      {
        server: containerRegistry.properties.loginServer
        username: containerRegistry.listCredentials().username
        password: containerRegistry.listCredentials().passwords[0].value
      }
    ]
    osType: 'Linux'
    restartPolicy: 'Never'
  }
}
