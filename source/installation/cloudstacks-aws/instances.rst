.. _aws-cloudstacks-instances:

Instances
#########

Fleet Manager manages three kinds of DSS instances:

* Design nodes
* Execution (aka automation) nodes
* Deployer nodes (usually you only have a single deployer node in your fleet)

Dashboard
=========

The main screen through which you will get information about your instance is the dashboard. It is refreshed automatically
and displays basic network information, data disk usage as well as the :ref:`agent <cloudstacks-concept-agent>` logs.

.. _cloudstacks-instance-lifecycle:

Lifecycle
=========

Provisioning
------------

The provisioning is the sequence of operations required to have a running DSS reachable by users. Provisioning an instance
has two main stages:

- The provisioning of cloud resources required for the instance to run. It is mostly a virtual machine and a data disk.
- A software startup sequence run by the :ref:`agent <cloudstacks-concept-agent>` which runs internal setup tasks, the setup actions you
  defined in your instance template, and installs and upgrades DSS if required.

Some settings changes require that you deprovision an instance an provision it again, which is denoted as *reprovisioning*.

Deprovisioning
--------------

Deprovisioning an instance consists of terminating the cloud virtual machine. The EBS is kept. A deprovisioned instance costs the EBS storage fee.

Data management
===============

When an instance is created, a data disk distinct from the OS disk is created, attached and mounted to store all the persistent
data. The persistent data on an instance includes, but is not limited to:

- The DSS data directory
- The docker daemon data directory
- The certificates generated if self-signed certificates or Let's Encrypt certificates are in use.

Settings
========

An instance has various settings that can be set at different point of its lifecycle.

General settings
----------------

Not documented yet

SSL settings
------------

The SSL settings define how your DSS instance will be exposed over SSL. This varies depending on the value you choose for HTTPS strategy in your virtual network:

None (HTTP only)
^^^^^^^^^^^^^^^^

SSL will be disabled and your DSS instance will be accessible by HTTP only. No SSL settings are required.


Self-signed certificates
^^^^^^^^^^^^^^^^^^^^^^^^

A self-signed certificate will be generated when the DSS instance is installed. Self-signed means that no official certificate authority has signed this certificate. Your DSS instance will be accessible over HTTPS, but the certificate won't be trusted by your users by default. Each user will need to manually trust the self-signed certificate. We only recommend this HTTPS strategy if all DSS users are familiar and comfortable with trusting a self signed certificate.

To make this mode more convenient, in the SSL settings, you can define the hostnames that will be injected in the self-signed certificate as `Subject Alternative Name`. This is required if you define a hostname pointing to the DSS instance and you want your users to access DSS via this hostname instead. Each user will still need to trust this certificate manually, but once done, their browser will accept the connection to this DSS instance using the hostname defined as `Subject Alternative Name`.

Certificate/key for each instance
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This strategy will allow you to manually define a certificate for each instance, in the SSL settings of the instance.

The advantage is that you can use a certificate signed by an official certificate authority and for a given hostname you own, so your users can access the DSS instance via this hostname and see the given certificate as trusted by their browser.

Generating or retrieving such certificate is not documented here, as this process generally depends on your company policy. Please ask your IT department on how to get a trusted certificate.

Once you have a certificate, the SSL settings offer three storage modes:

Enter key
"""""""""

The certificate will be stored in Fleet Manager, encrypted with a key from your AWS Key Management Service (KMS) and retrieved by the DSS instance at startup.

The format expected is PEM, for both the public and private key. If you don't have the certificate in this format, please use OpenSSL accordingly.

The private key will be encrypted with your AWS KMS, so you will need to configure the Key Vault.

Create a key for encryption in your Key Vault:

- Go to your AWS KMS, ideally in the same region than your FM
- Click on `Create key`
- Choose a `Symmetric` key type for a `encrypt and decrypt` usage
- Click `Next`
- Define the alias of your choice, like `FMKey`
- Click `Next`
- Choose your FM role (that's the role you assigned to FM during the provisioning of FM, under the reference `fm-role-name`)
- Click `Next`
- Choose your FM role
- Click `Next`
- Click `Finish`
- Copy the key ID. In the rest of this document, this role name will be noted as `fm-kms-key-id`

Then in FM, setup the Key vault:

- Go in "Cloud Setup > Edit"
- Set the "AWS CMK Id" to `fm-kms-key-id` (AWS KMS is replacing the term customer master key (CMK) with AWS KMS key and KMS key)
- Click `Save`


Your fleet manager is now ready to handle manual certificates. In your instance settings, in the SSL section:

- Set the public PEM and private PEM

Secret stored in Key Vault
""""""""""""""""""""""""""

The certificate public PEM will be stored in FM, whereas the private key will be stored as an AWS secret.

In AWS:
- Go to the AWS Secret Manager in the same zone than your DSS instance.
- Click on `Store a new secret`
- Select the type `Other type of secret`
- Select the format `Plaintext`
- Replace the sample text by your certificate private key as PEM
- Click `Next`
- Put a secret name. In the rest of this document, this role name will be noted as `dss-cert-secret-name`
- Click `Next`
- Click `Next`
- Click `Store`

In AWS IAM

Verify that your DSS role (referred as `dss-role-name` in the FM provisioning documentation) has the secret manager role.
- Go to the AWS IAM
- Find your DSS role `dss-role-name`
- Verify if any of the policy has the permission `secretsmanager:*`. If not, add it to one of the policy and save.
- Take note of the “Instance profile ARN”. In the rest of this document, it will be noted as `dss-role-instance-profile-arn`

In Fleet manager, SSL settings, configure the instance as follows:

- **Key storage mode**: Secret stored in ASM
- **SSL certificate (PEM data)**: The public certificate as PEM
- **ASM secret id**: `dss-cert-secret-name`
- **ASM Region**: This field is deprecated and will be remove in future release. You can ignore this value.

.. note::

  In the instance template, make sure the `Runtime instance profile ARN` is setup to `dss-role-instance-profile-arn`, otherwise the agent won't be able to access the key vault.

Provision or reprovision your DSS instance. At startup, the certificate will be retrieved from the AWS Secret Manager and you will notice that your DSS instance is now exposed using this certificate.

Generate certificates using Let's Encrypt
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

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
==========

Not documented yet
