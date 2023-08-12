param location string = resourceGroup().location
param environmentType string = 'prod'

var containerRegistryName = 'tgtgcontainerregistry${environmentType}'

resource containerRegistry 'Microsoft.ContainerRegistry/registries@2022-12-01' = {
  name: containerRegistryName
  location: location
  sku: {
    name: 'Basic'
  }
  properties: {
    adminUserEnabled: true
  }
}
