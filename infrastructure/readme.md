# Infrastructure as code Bicep template

## Usage
1. Create a resource group and set the default resource group using the Azure CLI:
```
az configure --defaults group={your-resource-group-name}
```

2. Run the `container-registry.bicep` file using the Azure CLI. This will create the container registry where your Docker image will be stored.
```
az deployment group create --template-file container-registry.bicep
```

3. Build the docker image and make sure you can run it locally:
```
docker build -t toogoodtogo-notifier .
docker run --env-file src/.development.env toogoodtogo-notifier
```

4. Tag & push the docker image to the container registry
```
docker tag toogoodtogo-notifier tgtgcontainerregistryprod.azurecr.io/tgtg/service
az acr login --name tgtgcontainerregistryprod
docker push tgtgcontainerregistryprod.azurecr.io/tgtg/service
```

5. Enter the parameter values in the `container-instance.bicepparam` bicep parameter file, such as your SendGrid settings and/or Telegram settings.

6. Run the `container-instance.bicep` file using the Azure CLI. This will create the container instance where your Docker image will run.
```
az deployment group create --template-file .\container-instance.bicep --parameters container-instance.bicepparam
```