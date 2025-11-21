Salesforce
#############
These tools are provided by the "Salesforce" plugin, which needs to be installed.

Lookup Salesforce Account
=========================

This tool looks up a Salesforce account by name.

In the plugin Settings create a new preset to connect to a Salesforce instance with Single Sign-On (SSO) or username/password.

When configuring a tool instance in a project, choose a preset.

The tool can look up the following account attributes: Id, Name, Website, Industry, Phone, Type, BillingCity, BillingCountry.

Test your Lookup Salesforce Account tool in the "Quick test" tab:

.. code-block:: json

    {
        "input": {
            "Name": "Account Name"
        },
        "context": {}
    }


Create Salesforce Contact
=========================

This tool creates a new Salesforce contact.

In the plugin Settings create a new preset to connect to a Salesforce instance with Single Sign-On (SSO) or username/password.

When configuring a tool instance in a project, choose a preset.

The tool can create a contact with a FirstName and LastName, and optionally the following attributes: Salutation, Email, Title, Department, AssistantName, LeadSource, Birthdate, MailingStreet, MailingCity, MailingState, MailingPostalCode, MailingCountry, Phone, MobilePhone, AccountName, Website.

Test your Create Salesforce Contact tool in the "Quick test" tab:

.. code-block:: json

    {
        "input": {
            "LastName": "ContactLastName",
            "FirstName": "ContactFirstName",
            "Salutation": "Dr.",
            "Email": "person@company.com",
            "Title": "CTO",
            "Department": "Engineering",
            "AssistantName": "None",
            "LeadSource": "Web",
            "Birthdate": "1990-01-01",
            "MailingStreet": "125 W 25th St",
            "MailingCity": "New York",
            "MailingState": "NY",
            "MailingPostalCode": "12345",
            "MailingCountry": "USA",
            "Phone": "1-800-000-0000",
            "MobilePhone": "1-800-000-0000",
            "AccountName": "Account Name",
            "Website": "company.com"
        },
        "context": {}
    }
