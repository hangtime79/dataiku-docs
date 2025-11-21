# Secrets fetchers

  * [1. AWS](#AWS)
  * [2. Azure](#Azure)
  * [3. GCP](#GCP)

  
This app note explains how to fetch the DSS config key from a secret manager. We will cover the different authentication modes and how to configure your application to use these secrets.

<a name="AWS"></a>

## AWS

### Create an IAM Role

First, create an IAM role with the necessary permissions:
1. Navigate to IAM in the AWS Management Console.
2. Create a new role with the following policies:
   - `SecretsManagerReadWrite`
   - `IAMFullAccess`
   
Attach this role to your DDS instance.

### Add the Config Key to AWS Secrets Manager

DSS will use the default AWS credentials.

1. Go to **Secrets Manager** in the AWS Management Console.
2. Add a new secret with the following details:
   - **Name**: `dsskey`
   - **Secret Value**: Use the whole content of the `config/configkey.json` file.

### Configure DSS to use AWS Secrets Manager

To configure DSS to use AWS Secrets Manager for secret management, edit the `dip.properties` file and add the following properties.

```
dku.passwordEncryption.provider.class=com.dataiku.dip.security.AWSSMBasedSymetricKeyBasedPasswordEncryptionProvider
dku.passwordEncryption.provider.settings={ "secretFormat" : "B64_JSON_KEY", "jsonKey" : "key", "secretName" : "dsskey" }
```
#### Documentation of `dku.passwordEncryption.provider.settings` JSON fields

- `"jsonKey`:  the key of JSON field that contains the encryption key. Usually used if the Secret Manager has the whole content of `config/configkey.json`. Default is `key`
- `"secretFormat`: the format of your key `B64_STRING`, `RAW_BYTES` or `B64_JSON_KEY`. Default is `B64_JSON_KEY` (usually used if the Secret Manager has the whole content of `config/configkey.json`)
- `"secretName`: the name of the secret created in AWS Secret Manager

Restart DSS so the new configuration is picked up.

By following these steps, your application will be able to securely access secrets stored in AWS secret manager.

<a name="Azure"></a>

## Azure

### Create an App
First, create an application in Azure Active Directory.

### Add the Permissions
1. Navigate to your app registration.
2. Add the following permissions: **Azure Key Vault** in delegated mode.

Copy your OAuth2 credentials for later use.

Depending on your security requirements, you can use either secret authentication mode or certificate authentication mode to authenticate your application.

#### Secret Auth Mode
1. Create a secret in your app registration.
2. Note down the secret value; you will use it as `clientSecret` later in your application configuration.

#### Certificate Auth Mode
1. Upload a certificate to your app registration.
2. Note down the certificate path and password; you will use `certificatePath` and `password` later in your application configuration.

### Configure Your KeyVault

1. Go to **IAM** (Identity and Access Management) in your Key Vault.
2. Add the roles:
   - `Key Vault Reader`
   - `Key Vault Secrets User`

#### Adding a Secret

1. Navigate to the **Secrets** section in your Key Vault.
2. Add a new secret with the name `dsskey`.
3. As the value, use the `key` content from your `config/configkey.json` file.

### Setting Up DSS 

To configure DSS to use Azure Key Vault for secret management, edit the `dip.properties` file and add the relevant properties based on the authentication mode you chose.

#### Secret Auth Mode

```
dku.passwordEncryption.provider.class=com.dataiku.dip.security.AzureKeyvaultBasedSymetricKeyBasedPasswordEncryptionProvider
dku.passwordEncryption.provider.settings={ "clientId" : "d09d96a9-b6e4-4c70-846d-577f02c15b6f", "domain": "3ceb0d29-d7de-4204-b431-3f9f8edb2106", "clientSecret" : "xxxxx", "kevaultName": "secretfetcher-qcastel", "secretName" : "dsskey" }
```

#### Certificate Auth Mode

```
dku.passwordEncryption.provider.class=com.dataiku.dip.security.AzureKeyvaultBasedSymetricKeyBasedPasswordEncryptionProvider
dku.passwordEncryption.provider.settings={ "clientId" : "d09d96a9-b6e4-4c70-846d-577f02c15b6f", "domain": "3ceb0d29-d7de-4204-b431-3f9f8edb2106", "certificatePath" : "/data/dataiku/dss_data/dss.dataiku.io.pfx", "password": "changeit",  "kevaultName": "secretfetcher-qcastel", "secretName" : "dsskey" }
```

#### Managed Identity Mode

```
dku.passwordEncryption.provider.class=com.dataiku.dip.security.AzureKeyvaultBasedSymetricKeyBasedPasswordEncryptionProvider
dku.passwordEncryption.provider.settings={ "clientId" : "d09d96a9-b6e4-4c70-846d-577f02c15b6f", "domain": "3ceb0d29-d7de-4204-b431-3f9f8edb2106", "managedIdentityId": "/subscriptions/8c59bf15-b4a9-4398-a354-d2a4e7d60e2a/resourceGroups/qcastel-fm/providers/Microsoft.ManagedIdentity/userAssignedIdentities/secretfetcher-dss-id",  "kevaultName": "secretfetcher-qcastel", "secretName" : "dsskey" }
```

Restart DSS.

By following these steps, your application will be able to securely access secrets stored in Azure Key Vault using the chosen authentication method.

<a name="GCP"></a>

## GCP

Note: supported from 13.2.0 only

### Authentication Modes

DSS will use the default GCP credentials.

### Configure Your Secret Manager

1. Go to **Secret Manager** in the Google Cloud Console.
2. Add a new secret with the following details:
   - **Name**: `dsskey`
   - **Secret Value**: Use the `key` content from your `config/configkey.json` file.
3. Make sure the service account used by DSS is able to access your key

### Setting Up DSS

To configure DSS to use Google Cloud Secret Manager for secret management, edit the `dip.properties` file and add the relevant properties based on the authentication mode you chose.
 
```
dku.passwordEncryption.provider.class=com.dataiku.dip.security.GCPSecretsFetcherBasedSymetricKeyBasedPasswordEncryptionProvider
dku.passwordEncryption.provider.settings={ "projectId": "qcastel-secretfetcher-20240626", "secretName" : "dsskey" }
```

- `"projectId`:  the project ID of your KMS
- `"secretName`: the name of your secret

Restart DSS.

By following these steps, your application will be able to securely access secrets stored in Google Cloud Secret Manager.
