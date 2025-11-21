High availability
#################

Fleet Manager enables high availability for automation nodes.

Load balancing
==============

Fleet Manager manages load balancers.

When defining load balancer node mappings, a single hostname can be associated with multiple automation nodes to enable load balancing between them.

Deployer infrastructures
========================

When an automation node is added to a fleet containing a deployer node, the necessary infrastructure is automatically created in the deployer node to allow deployments to the new automation node.

If the **Create a single-node infrastructure** option is enabled on the automation node, a single-node infrastructure will be created, allowing deployments only to this node.

If the automation node is placed behind a load balancer, a multi-node infrastructure will be created. As additional nodes are added behind the same hostname, the multi-node infrastructure will expand accordingly. This setup enables deployments to all nodes that make up the high-availability infrastructure simultaneously.
