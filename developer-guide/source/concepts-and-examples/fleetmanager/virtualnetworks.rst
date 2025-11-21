Fleet Manager Virtual Networks
##############################

A virtual network allows instances to communicate with each other.

Create a new virtual network
============================

.. code-block:: python

    import dataikuapi

    key_id = "<my key id>"
    key_secret = "<my key secret>"

    # <Cloud vendor> is either AWS, Azure or GCP
    client = dataikuapi.FMClient<Cloud vendor>("https://localhost", key_id, key_secret)
    creator = client.new_virtual_network_creator("MyNetwork")
    # set the properties of your network
    ...
    network = creator.create()


Reference documentation
=======================

.. autosummary:: 
    dataikuapi.fm.virtualnetworks.FMVirtualNetwork
    dataikuapi.fm.virtualnetworks.FMVirtualNetworkCreator
    dataikuapi.fm.virtualnetworks.FMAWSVirtualNetwork
    dataikuapi.fm.virtualnetworks.FMAWSVirtualNetworkCreator
    dataikuapi.fm.virtualnetworks.FMAzureVirtualNetwork
    dataikuapi.fm.virtualnetworks.FMAzureVirtualNetworkCreator
    dataikuapi.fm.virtualnetworks.FMGCPVirtualNetwork
    dataikuapi.fm.virtualnetworks.FMGCPVirtualNetworkCreator
    dataikuapi.fm.virtualnetworks.FMHTTPSStrategy