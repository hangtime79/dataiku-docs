.. _azure-cloudstacks-instances:

Instances
###########

Fleet Manager manages three kinds of DSS instances:

* Design nodes
* Execution (aka automation) nodes
* Deployer nodes (usually you only have a single deployer node in your fleet)

Dashboard
==========

The main screen through which you will get information about your instance is the dashboard. It is refreshed automatically
and displays basic network information, data disk usage as well as the :ref:`agent <azure-cloudstacks-concept-agent>` logs.

.. _azure-cloudstacks-instance-lifecycle:

Lifecycle
===========

Provisioning
--------------

The provisioning is the sequence of operations required to have a running DSS reachable by users. Provisioning an instance
has two main stages:

- The provisioning of cloud resources required for the instance to run. It is mostly a virtual machine and a data disk.
- A software startup sequence run by the :ref:`agent <azure-cloudstacks-concept-agent>` which runs internal setup tasks, the setup actions you
  defined in your instance template, and installs and upgrades DSS if required.

Some settings changes require that you deprovision an instance and provision it again, which is denoted as *reprovisioning*.

Deprovisioning
----------------

Deprovisioning an instance consists of terminating the cloud virtual machine. The Persistent Disk is kept. A deprovisioned instance costs the Persistent Disk storage fee.

Data management
================

When an instance is created, a data disk distinct from the OS disk is created, attached and mounted to store all the persistent
data. The persistent data on an instance includes, but is not limited to:

- The DSS data directory
- The docker daemon data directory
- The certificates generated if self-signed certificates or Let's Encrypt certificates are in use.

Settings
==========

An instance has various settings that can be set at different point of its lifecycle.

General settings
-----------------

Not documented yet

SSL settings
----------------

The SSL settings define how your DSS instance will be exposed over SSL. This varies depending on the value you choose for HTTPS strategy in your virtual network:

None (HTTP only)
^^^^^^^^^^^^^^^^^^^^

SSL will be disabled and your DSS instance will be accessible by HTTP only. No SSL settings are required.


Self-signed certificates
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A self-signed certificate will be generated when the DSS instance is installed. Self-signed means that no official certificate authority has signed this certificate. Your DSS instance will be accessible over HTTPS, but the certificate won't be trusted by your users by default. Each user will need to manually trust the self-signed certificate. We only recommend this HTTPS strategy if all DSS users are familiar and confortable with trusting a self signed certificate.

To make this mode more convenient, in the SSL settings, you can define the hostnames that will be injected in the self-signed certificate as `Subject Alternative Name`. This is required if you define a hostname pointing to the DSS instance and you want your users to access DSS via this hostname instead. Each user will still need to trust this certificate manually, but once done, their browser will accept the connection to this DSS instance using the hostname defined as `Subject Alternative Name`.

Certificate/key for each instance
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This strategy will allow you to manually define a certificate for each instance, in the SSL settings of the instance.

The advantage is that you can use a certificate signed by an official certificate authority and for a given hostname you own, so your users can access the DSS instance via this hostname and see the given certificate as trusted by their browser.

Generating or retrieving such certificate is not documented here, as this process generally depends on your company policy. Please ask your IT departement on how to get a trusted certificate.

Once you have a certificate, the SSL settings offer three storage modes:

Enter key
""""""""""""""""""""""""""

The certificate will be stored in Fleet Manager, encrypted with a key from your Azure Key Vault and retrieved by the DSS instance at startup.

The format expected is PEM, for both the public and private key. If you don't have the certificate in this format, please use OpenSSL accordingly.

The private key will be encrypted with your Azure Key Vault, so you will need to configure the Key Vault.

Create a key for encryption in your Key Vault:

- Go to your Azure Key Vault portal
- Go to the "Keys" section on the left navigation
- Create a new RSA key and give it a name that we will refer to as ``encryption-key-name``. The version of the key will also be needed later, which we will refer to as ``encryption-key-version``
- Click on "Access policies" to give the permissions to the FM and DSS managed identities so that they can access the key
- Click on "Add access policy"
- Give the "Cryptographic Operations" permissions to the FM and DSS managed identities, as well as the "Get" key management operations

Then in FM, setup the Key vault:

- Go in "Cloud Setup > Edit"
- Set the "Encryption KeyVault Id", it's the resource ID corresponding to your Azure Key vault. Example: ``/subscriptions/YOUR_SUBSCRIPTION_ID/resourceGroups/YOUR_RESOURCE_GROUP/providers/Microsoft.KeyVault/vaults/KEY_VAULT_NAME``
- Set the "Encryption Key Name" to ``encryption-key-name``
- Set the "Encryption Key Version" to ``encryption-key-version``

Your fleet manager is now ready to handle manual certificates. In your instance settings, in the SSL section:

- Set the public PEM and private PEM

Secret stored in Key Vault
""""""""""""""""""""""""""""""

.. WARNING:: This mode is now deprecrated by Azure. Azure advises to switch to `Certificate stored in Key Vault` instead.

The certificate public PEM will be stored in FM, whereas the private key will be stored as an Azure Key Vault secret.

Create a new Secret in Azure Key Vault with the private key as 1) PEM and 2) base64 encoded (important). Give to the DSS managed identity the READ permissions to the secret Key Vault.

In Fleet manager, SSL settings, configure the instance as follows:

- **Key storage mode**: Secret stored in Azure Key Vault
- **SSL certificate (PEM data)**: The public certificate as PEM
- **Keyvault Url**: The vault URI, you can find it in your Key Vault dashboard. It usually looks like ``https://YOUR_VAULT_NAME.vault.azure.net/``
- **Secret Name**: Secret name you defined for the private key
- **Secret version**: Secret version for the private key. If not defined, the latest version of the certificate will be taken.
- **User Assigned Managed Service Identity Resource Id**: The resource ID of the DSS managed identity. Example: ``/subscriptions/YOUR_SUBSCRIPTION_ID/resourceGroups/YOUR_RESOURCE_GROUP/providers/Microsoft.ManagedIdentity/userAssignedIdentities/YOUR_DSS_MANAGED_IDENTITY_NAME``
- **User Assigned Managed Service Client Id**: The client ID of the DSS managed identity. This can be found in the dashboard of the managed identity.

Provision or reprovision your DSS instance. At startup, the certificate will be retrieved from the Azure Key Vault and you will notice that your DSS instance is now exposed using this certificate.

Certificated stored in Key Vault
""""""""""""""""""""""""""""""""""""""

The certificate will be stored entirely into the Azure certificate Key vault.

Import or create a new certificate in Azure Key Vault, see the Azure documentation for more details. Remember the "Content Type" you selected for this certificate, this will be necessary for the SSL settings in FM.

Give to the managed identity of DSS the READ permissions to the secret Key Vault.

In Fleet manager, in the SSL settings of the instance, configure as follows:

- **Key storage mode**: Certificate stored in Azure Key Vault
- **Keyvault Url**: The vault URI, you can find it in your key vault dashboard. It usually looks like ``https://YOUR_VAULT_NAME.vault.azure.net/``
- **Certificate name**: The certificate name in the Azure certificate Key Vault
- **Certificate version**: The certificate version in the Azure certificate Key Vault. If not defined, the latest version of the certificate will be taken.
- **Certificate Content Type**: The content type you selected when storing the certificate in Azure Key vault
- **User Assigned Managed Service Identity Resource Id**: The resource ID of the DSS managed identity. Example: ``/subscriptions/YOUR_SUBSCRIPTION_ID/resourceGroups/YOUR_RESOURCE_GROUP/providers/Microsoft.ManagedIdentity/userAssignedIdentities/YOUR_DSS_MANAGED_IDENTITY_NAME``
- **User Assigned Managed Service Client Id**: The client ID of the DSS managed identity. This can be found in the dashboard of the managed identity.

Provision or reprovision your DSS instance. At startup, the certificate will be retrieved from the Azure Key Vault and you will notice that your DSS instance is now exposed using this certificate.


Generate certificates using Let's Encrypt
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

`Let's Encrypt` is a certificate authority, trusted by default by most browsers, which offers a certificate service for free, given you own a domain. This means that `Let's Encrypt` can generate a certificate for your DSS instance, if you point your domain hostname to the DSS IP.

.. note:: Prerequisites

  You need to own a domain, like ``mydss.example.com`` and point the DNS A record to a public static IP. This IP will then be assigned to the DSS instance.

In Fleet manager, on the virtual network, settings tab:

- setup the `SSL > Strategy` to `Generate certificates using Let's Encrypt`
- setup the `Contact Mail` to an email address of your choice

In Fleet manager, on the instance page, settings tab, configure the instance as follows:

- in the SSL part, click on `+ ADD DOMAIN`
- Add the hostname of your domain. Example: ``mydss.example.com``
- Assign the public IP to this instance.

Provision the DSS instance. When completed, you should be able to access your DSS instance with ``https://mydss.example.com`` and see a valid HTTPs certificate signed by `Let's Encrypt`.

Operations
============

Not documented yet
