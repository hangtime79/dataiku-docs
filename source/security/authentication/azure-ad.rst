Azure AD
###############

.. note::

  DSS Azure AD implementation is only a User Supplier. See :doc:`Authentication </security/authentication/index>` documentation for more details.


The DSS Azure AD User Supplier allows the provisioning or synchronization of Azure AD users in DSS. However, it is important to note that the DSS Azure AD User Supplier cannot authenticate users, as it is not possible to retrieve user passwords from Azure AD or authenticate users using the Azure AD API.

To authenticate users, it is necessary to combine the DSS Azure AD User Supplier with another authentication method, such as SSO.

Configuration
*********************

DSS connects to Azure AD using OAuth2, using either a secret or a certificate.

Azure portal
=====================

In your company's Azure AD portal, follow these steps:

- Go to your Azure Active Directory > App registrations
- Create a new application dedicated to DSS, with no redirect URI specified (DSS uses the client credential flow to connect to Azure AD).
- Add the required credentials (`secrets` or `certificates`) in the application settings. DSS supports both types.
- Grant the following Application permissions in the API permissions section:
    -  `Microsoft Graph` -> `Group.Read.All`
    -  `Microsoft Graph` -> `User.Read.All`

Make sure to note down the tenant ID, client ID, client secret, or certificates, as these will be needed for the DSS configuration.


DSS security settings
=====================

In DSS in the `Settings` > `Security & Audit` > `User login & provisioning` > `Azure AD` section:

- Enable Azure AD
- Depending on your requirements, choose to :ref:`enable user provisioning, user synchronization, or both <synchronizing-user-attributes>`.


Connection credential
---------------------
- Select the credential mode:
    - `Secret` if you configured the Azure application to use a `client secret` as a credential
    - `Certificate` if you configured the Azure application to use a `certificate` as a credential
- Fill in the other values in the "credential" section as per the Azure portal configuration. These values should be self-explanatory.


User Mapping
---------------------

- `User query filter`: Specify the Azure AD query for the `/users` endpoint, which DSS will use to find users matching the specified identity. You can use simple queries like `mail eq '$email'`, `userPrincipalName eq '$login'`, `startsWith(userPrincipalName,'$login')`, or `startsWith(mail,'$login')`. You can test your query using cURL commands or directly in the DSS UI's testing mode.
- `Groups restriction`: If this list is not empty, only users who are members of one of these groups in Azure will be authorized to connect to the DSS instance.


On-Demand Provisioning
-----------------------

- `Allow on-demand provisioning`: When enabled, a new view is added to the administration security settings, allowing you to fetch Azure AD users before provisioning/synchronizing them. On-demand provisioning is only available for admin users.
- `Login attribute`: This is the Azure AD user attribute used as the username for the newly provisioned user.
- `Login remapping rules`: The Azure AD login attribute may require remapping before being used as a DSS username. You can define remapping rules as search-and-replace Java regular expressions. Use ``(...)`` to capture substrings and ``$1``, ``$2``, etc., to insert the captured substrings in the output. The rules are applied in order, with each rule operating on the output of the previous one.

User Profiles
-------------

- `Group → profile mapping`: Define a mapping from Azure AD group names to DSS user profiles. The rules are evaluated in order until a match is found.
- `Default user profile`: This is the default profile assigned to any new user if no profile can be computed from their groups. See :ref:`mapping-profiles-and-groups`.

Testing
--------

The testing section provides a way to simulate the identity and check the DSS Azure AD User supplier results. The simulation results will also show the computed DSS groups, allowing you to verify that a user will be assigned to the expected DSS groups.

.. _azure-ad-permissions:

Permissions
-----------

- `Azure AD groups readable by`: this setting, if set to the option `Everybody`, allows all users, who run the list access recipe, to access the mappings between Azure AD groups and DSS groups defined by DSS admins.

Troubleshooting
***************

If you encounter any problems configuring AzureAD in DSS, you can manually check your Azure AD configuration. Note that the following testing instructions only apply to the client secret authentication method.

Follow these steps:

- Create an access token using the provided cURL command.

.. code-block:: bash

    curl --location --request POST 'https://login.microsoftonline.com/$YOUR_TENANT_ID/oauth2/v2.0/token' \
    --header 'Accept: application/json' \
    --header 'Content-Type: application/x-www-form-urlencoded' \
    --data-urlencode 'grant_type=client_credentials' \
    --data-urlencode 'scope=https://graph.microsoft.com/.default' \
    --data-urlencode 'client_id=$YOUR_CLIENT_ID' \
    --data-urlencode 'client_secret=$YOUR_CLIENT_SECRET'


If your application is properly set up, you should receive a successful response with an access token.

.. code-block:: json

    {
        "token_type": "Bearer",
        "expires_in": 3599,
        "ext_expires_in": 3599,
        "access_token": "AZURE_ACCESS_TOKEN"
    }


Verify the roles in the access token payload by introspecting it using https://jwt.io/. You should see the roles in the payload:

.. code-block:: json

    {
        "roles": [
            "Group.Read.All",
            "User.Read.All"
        ]
    } 


To confirm that your access token has indeed the permissions to read users and groups, you can try the following requests:

.. code-block:: bash

    curl --location --request GET 'https://graph.microsoft.com/v1.0/users?$filter=mail eq '\''alice@example.com'\''' \
    --header 'Authorization: Bearer $AZURE_ACCESS_TOKEN'

You should be able to query users, with a typical response looking like:

.. code-block:: json

    {
        "@odata.context": "https://graph.microsoft.com/v1.0/$metadata#users",
        "value": [
            {
                "businessPhones": [],
                "displayName": "Alice Doe",
                "givenName": null,
                "jobTitle": null,
                "mail": "alice@example.com",
                "mobilePhone": null,
                "officeLocation": null,
                "preferredLanguage": null,
                "surname": null,
                "userPrincipalName": "alice",
                "id": "ee0a9719-5dd0-46a1-93de-cad4455f2863"
            }
        ]
    }

You can test the group permissions by querying the groups for a given user:

.. code-block:: bash

    curl --location --request GET 'https://graph.microsoft.com/v1.0/users/e0a9719-5dd0-46a1-93de-cad4455f2863/memberOf/microsoft.graph.group' \
    --header 'Authorization: Bearer $AZURE_ACCESS_TOKEN'


You should see the groups for this user, with a typical response looking like:

.. code-block:: json

    {
        "@odata.context": "https://graph.microsoft.com/v1.0/$metadata#groups",
        "value": [
            {
                "id": "b2771f37-441f-4485-7b78-cfeeed03cd8b",
                "deletedDateTime": null,
                "classification": null,
                "createdDateTime": "2021-11-03T15:26:08Z",
                "creationOptions": [],
                "description": null,
                "displayName": "group_a",
                "expirationDateTime": null,
                "groupTypes": [],
                "isAssignableToRole": null,
                "mail": null,
                "mailEnabled": false,
                "mailNickname": "group_a",
                "membershipRule": null,
                "membershipRuleProcessingState": null,
                "onPremisesDomainName": null,
                "onPremisesLastSyncDateTime": null,
                "onPremisesNetBiosName": null,
                "onPremisesSamAccountName": null,
                "onPremisesSecurityIdentifier": null,
                "onPremisesSyncEnabled": null,
                "preferredDataLocation": null,
                "preferredLanguage": null,
                "proxyAddresses": [],
                "renewedDateTime": "2021-11-03T15:26:08Z",
                "resourceBehaviorOptions": [],
                "resourceProvisioningOptions": [],
                "securityEnabled": true,
                "securityIdentifier": "S-1-12-1-eeee-1132807199-eeee-333",
                "theme": null,
                "visibility": null,
                "onPremisesProvisioningErrors": []
            }
        ]
    }
