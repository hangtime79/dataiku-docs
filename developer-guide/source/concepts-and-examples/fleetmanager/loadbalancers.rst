Load Balancers
##############

Load balancers act as application gateways in front of Dataiku nodes. They can also be used to perform load balancing in front of automation nodes to achieve high availability.

Create a load balancer
======================


.. code-block:: python

    import dataikuapi

    key_id = "<my key id>"
    key_secret = "<my key secret>"

    # <Cloud vendor> is either AWS or Azure
    client = dataikuapi.FMClient<Cloud vendor>("https://localhost", key_id, key_secret)

    my_network_id = "vn-default"

    # create a load balancer
    creator = client.new_load_balancer_creator("My load balancer", my_network_id)

    # set the load balancer properties
    ...

    load_balancer = creator.create()
    status = load_balancer.reprovision()
    res = status.wait_for_result()


Reference documentation
=======================

.. autosummary::
    dataikuapi.fm.loadbalancers.FMLoadBalancer
    dataikuapi.fm.loadbalancers.FMLoadBalancerCreator
    dataikuapi.fm.loadbalancers.FMLoadBalancerPhysicalStatus
    dataikuapi.fm.loadbalancers.FMAWSLoadBalancer
    dataikuapi.fm.loadbalancers.FMAWSLoadBalancerCreator
    dataikuapi.fm.loadbalancers.FMAzureLoadBalancer
    dataikuapi.fm.loadbalancers.FMAzureLoadBalancerCreator
    dataikuapi.fm.loadbalancers.FMAzureLoadBalancerTier
