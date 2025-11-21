Passwords security
###################

.. contents::
	:local:

Local passwords database or not
=================================

DSS comes with its own local passwords database. When an administrator creates a user (through Administration > Security > Users), and creates a "Local" user, the password is stored encrypted in the local passwords database.

In most enterprise deployments, however, the local passwords database isn't used. Instead, users come from a LDAP directory. Users can then login directly on DSS with their LDAP password, or use SSO to login + LDAP to fetch groups.

Passwords complexity
=====================

DSS does not mandate any password security rules for the passwords stored in the local passwords database. If you need password security rules enforced, we strongly recommend that you use LDAP instead of the local passwords database

Encryption of the local passwords database
============================================

Passwords in the local passwords database are encrypted using a one-way (non-reversible) hash function, which makes it extremely hard to find the original password from the encrypted hash.

The algorithm used is salted-PBKDF2, a state of the art hashing algorithm that is specifically designed to be resilient against brute-force attacks.

3rd party system credentials
=============================

In addition to the user passwords (in case the local passwords database is used), DSS also needs to keep passwords for all 3rd party systems it connects to:

* Passwords for SQL and NoSQL databases
* Cloud storages
* Integration credentials (Slack, ...)
* :doc:`User secrets <user-secrets>`
* ...

For all of these, unlike user passwords, DSS actually needs to have the decrypted password in order to send it to the 3rd party system.

These passwords are encrypted in the configuration files using a symmetric encryption algorithm. The algorithm used is authenticated AES in CTR mode. Both AES-128, AES-192 and AES-256 are supported. Authentication is performed by a HMAC-SHA256.

The encryption key is stored in the DSS data directory, and is never given out to DSS users.

Alternatively, the encryption key can be stored in your cloud secret manager (AWS Secrets Manager, Azure Key Vault or Google Cloud Secret Manager). Please reach out to your Dataiku Customer Success Manager to learn more.

Note that when using plugin "parameter sets", if you put the credentials inline in a dataset or recipe, they are not encrypted. Use "presets" instead.