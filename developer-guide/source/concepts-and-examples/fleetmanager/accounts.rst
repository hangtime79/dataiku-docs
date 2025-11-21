Fleet Manager Accounts
######################

Accounts are the different identities Fleet Manager can impersonate to manipulate cloud objects.

Create an account
=================

.. code-block:: python

    import dataikuapi

    key_id = "<my key id>"
    key_secret = "<my key secret>"

    # <Cloud vendor> is either AWS, Azure or GCP
    client = dataikuapi.FMClient<Cloud vendor>("https://localhost", key_id, key_secret)

    # create an account
    creator = client.new_cloud_account_creator("My new account")

    # Set the different parameters
    account = creator.create()


Reference documentation
=======================

.. autosummary::
    dataikuapi.fm.cloudaccounts.FMCloudAccount
    dataikuapi.fm.cloudaccounts.FMCloudAccountCreator
    dataikuapi.fm.cloudaccounts.FMAWSCloudAccount
    dataikuapi.fm.cloudaccounts.FMAWSCloudAccountCreator
    dataikuapi.fm.cloudaccounts.FMAzureCloudAccount
    dataikuapi.fm.cloudaccounts.FMAzureCloudAccountCreator
    dataikuapi.fm.cloudaccounts.FMGCPCloudAccount
    dataikuapi.fm.cloudaccounts.FMGCPCloudAccountCreator
