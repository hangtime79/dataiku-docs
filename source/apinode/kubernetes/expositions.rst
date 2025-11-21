Service expositions
###################

Once an API service is deployed in the cluster, there are pods running it and ready to serve HTTP requests on their port 12000. By design on Kubernetes, services running inside pods are not accessible from outside, where "outside" means "other pods in the cluster" and "anything outside the cluster". To make it possible to reach the API service, one needs to setup `Kubernetes services <https://kubernetes.io/docs/concepts/services-networking/service/>`_. The object through which you get DSS to create Kubernetes services is a `service exposition`, of which there are several types.

Load balancer
=============

A `Load balancer` exposition creates a service of type `LoadBalancer <https://kubernetes.io/docs/concepts/services-networking/service/#loadbalancer>`_ in the cluster. Not all clusters offer a native LoadBalancer service, but cloud providers typically have one, where they provision a Load balancer inside their infrastructure and set it up to route requests from outside the cluster all the way to the pods.

Cluster IP
==========

A `Cluster IP` exposition creates a service of type `ClusterIP <https://kubernetes.io/docs/concepts/services-networking/service/#type-clusterip>`_ in the cluster. The IP created by the Kubernetes service lives in the Kubernetes virtual network and is accessible from within the cluster only. This kind of service is mostly used to make the API service reachable by some other service or pod inside the cluster. In particular, this will not make it possible to query the API service from outside the cluster.

Node Port
=========

A `Node Port` exposition creates a service of type `NodePort <https://kubernetes.io/docs/concepts/services-networking/service/#type-nodeport>`_ in the cluster. This Kubernetes service exposes the API service on a fixed port on the nodes of the cluster. Like `Cluster IP`, it's mainly intended to make the API service accessible to other services or pods inside the cluster, not so much for making it available outside the cluster. You can reach it from outside the cluster only if you can reach the cluster nodes themselves.

Ingress
=======

An `Ingress` exposition creates a `Kubernetes Ingress <https://kubernetes.io/docs/concepts/services-networking/ingress/>`_ in the cluster, and a `Node Port` service underneath (this is a technicality, as ingresses need a NodePort or ClusterIP service to actually access the pods). Ingresses are the recommended method for exposing services from pods, but they usually require some extra setup:

- not all clusters have a default ingress controller, you may need to install one
- some ingress controllers need a Load balancer to be provisioned at the infrastructure level
- several ingresses can listen on the same load balancer and route to different API services, which requires careful handling of the ingresses' parameters

DSS offers some variants of the base `Ingress` exposition when they're available and DSS was notified of their existence:

- `Ingress (GKE)` is available when there is a ``cloud.provider -> gke`` entry in the custom properties of the container configuration used. It is tailored for `the native ingress in GKE clusters <https://cloud.google.com/kubernetes-engine/docs/concepts/ingress>`_.
- `Ingress (NGINX)`  is available when there is a ``nginx-ingress.controller -> true`` entry in the custom properties of the container configuration used. It is tailored for the `ingress controller built on top of NGINX <https://kubernetes.github.io/ingress-nginx/>`_ which you can install in the clusters of most cloud providers.

The most versatile of the ingress expositions is the `Ingress (NGINX)` one, and in practice, the only recommended exposition when you wish to deploy several API services on the same IP or hostname.

Ingress (NGINX)
---------------

To expose several API services on the same hostname/IP, assign a `Ingress (NGINX)` exposition to them, at the API deployment level or at the API infrastructure level. Then fill the **Service Path** field of the exposition with a different path for each API deployment, and tick the **Rewrite Path** checkbox.

.. note::

	While the NGINX ingress controller can handle TLS termination, the recommended setup is to handle the TLS termination at the load balancer layer, so as to have the ingress controller only handle `http://` requests.

Variables
---------

All expositions of the ingress kind can use variables in the **Service Path** field, in the annotations, and in the **Forced URL** field. These variables are used with the ``${variable_name}`` notation. In addition to the variables defined at the instance level, at the API infrastructure level and at the deployment level, several variables are available for use in API deployments:

- ``k8sDeploymentId`` : the name of the Kubernetes deployment of the API deployment
- ``apiDeploymentId`` and ``k8sFriendlyApiDeploymentId`` : the identifier of the API deployment
- ``infraId`` and ``k8sFriendlyInfraId`` : the identifier of the API infrastructure
- ``publishedServiceId`` and ``k8sFriendlyPublishedServiceId`` : the identifier of API service published by the API deployment
- ``deployedServiceId`` and ``k8sFriendlyDeployedServiceId`` : the identifier of the deployed API service (= contents of the **API service id once deployed** field of the API deployment)


The variables that have a ``k8sFriendlyXXXX`` variant have values that can make them not suitable as Kubernetes labels or annotations or names, because they don't follow the Kubernetes spec for these values. The ``k8sFriendlyXXXX`` variants are sanitized versions of the ``XXXX`` variable, and can be used in all fields of a Kubernetes object.

Arbitrary yaml
==============

This is the most versatile type of exposition. It lets you pass a yaml snippet to create objects in the cluster. The snippet can contain variables to aid in reusing the same snippet in several deployments, and the hostname/IP, port and path where DSS should find the deployed API service are defined in the yaml by means of hints in yaml comments.

.. note::

	The objects defined in the arbitrary yaml are created by DSS with the same credentials that it uses to deploy the API service.

Variables
---------

In addition to the variables defined at the instance level, at the API infrastructure level and at the deployment level, several variables are available for use in the yaml snippet:

- ``executionId`` : unique identifier for this run of the API deployment being deployed
- ``apiDeployerDeploymentId`` : unique identifier for the API deployment being deployed
- ``namePrefix`` : "dku-mad" in API deployments ("dku-webapp" in webapps)
- ``exposedPort`` : port inside the container that needs to be exposed
- ``labels`` : the DSS-generated K8S labels to associate to the API deployment being deployed (4-space padded)
- ``labelsJsonFields`` : the DSS-generated K8S labels as a JSON-encoded map, without the surrounding curly braces
- ``labelsHeader`` : use this to prefix the labels section. Empty if there are no K8S labels declared in the API deployment being deployed (2-space padded)
- ``labelsHeaderNoNewline`` : if there are DSS-generated K8S labels, then this is a 2-space padded "labels:" string
- ``annotations`` : `annotations`: K8S annotations declared in the API deployment being deployed. (4-space padded)
- ``annotationsJsonFields`` : K8S annotations declared in the API deployment as a JSON-encoded map, without the surrounding curly braces
- ``annotationsHeader`` : use this to prefix the annotations section. Empty if there are no K8S annotations declared in the API deployment being deployed (2-space padded)
- ``annotationsHeaderNoNewline`` : if there are K8S annotations eclared in the API deployment, then this is a 2-space padded "annotations:" string
- ``selector`` : K8S selector that will target the K8S deployment underlying the API deployment being deployed (4-space padded)
- ``selectorJsonFields`` : K8S selector as a JSON-encoded map, without the surrounding curly braces
- ``selectorHeader`` : a 2-spaces padded "selector:" line. Empty if the selector is empty
- ``selectorHeaderNoNewline`` :  2-spaces padded "selector:" string. Empty if the selector is empty
- ``deployment:prop_name`` : the value of the property `prop_name` on the API deployment being deployed


.. important::

	The ``executionId`` or ``apiDeployerDeploymentId`` being unique identifiers for the API deployment being deployed, they should be used in the ``metadata.name`` field of the Kuberenetes objects deployed, so as to avoid conflicts.


Extracting characteristics
--------------------------

Once the K8S objects are created, DSS needs to find them in the cluster in order to gather runtime information about them. A prime example of such information is the IP on which DSS should expect the API service to be exposed. For this to happen, you need to place hints inside the yaml snippet to flag lines where relevant information is located. These hints are put as fixed strings in comments. There are 2 cases:

1) if the yaml is creating a service to expose the API deployment, add ``# __exposed_service_id__`` behind the `metadata.name` field of a K8S service object
2) if the yaml is creating an ingress to expose the API deployment, add ``# __exposed_ingress_id__`` behind the `metadata.name` field of a K8S ingress object

When using an ingress, additional values can be passed:

- the scheme for the URL that DSS should use can be pointed to by means of a ``# __exposed_scheme__`` hint
- a path relative to the "scheme://host:port" can be passed with a ``# __exposed_service_path__`` hint
- if the "scheme://host:port" that DSS can infer from inspecting the K8S objects at runtime is not expected to be correct, a fixed value can be pointed to with a ``# __exposed_forced_url__`` hint.

All those hints apply to lines like:

.. code-block:: yaml

	some-field: the-value # __the_hint__

If you need to pass a value to a hint, but there is no field in the yaml whose semantic meaning corresponds to the value, you can use a commented line like:

.. code-block:: yaml

	# some-field: the-value # __the_hint__


Examples
--------

Exposing the API deployment with a load balancer provisioned by the cluster:

.. code-block:: yaml

	apiVersion: v1
	kind: Service
	metadata:
	  name: lb-${executionId} # __exposed_service_id__
	  labels: { ${labelsJsonFields} }
	  # add a load-balancer-type annotation on top of the DSS-computed annotations
	  annotations: { ${annotationsJsonFields}, "cloud.google.com/load-balancer-type":"Internal" }
	spec:
	  selector: { ${selectorJsonFields} }
	  type: LoadBalancer
	  ports:
	  - port: ${exposedPort}
	    targetPort: ${exposedPort}
	    protocol: TCP


Exposing the API deployment with an ingress from a NGINX-ingress controller and a ClusterIP service (instead of NodePort like the Ingress exposition):

.. code-block:: yaml

	apiVersion: v1
	kind: Service
	metadata:
	  name: svc-${executionId}
	  labels: { ${labelsJsonFields} }
	  annotations: { ${annotationsJsonFields} }
	spec:
	  selector: { ${selectorJsonFields} }
	  type: ClusterIP
	  ports:
	  - port: 12000
	    targetPort: 12000
	    protocol: TCP

	---
	apiVersion: networking.k8s.io/v1
	kind: Ingress
	metadata:
	  name: ing-${executionId} # __exposed_ingress_id__
	  labels: { ${labelsJsonFields} }
	  annotations: { ${annotationsJsonFields}, "kubernetes.io/ingress.class":"nginx", "nginx.ingress.kubernetes.io/rewrite-target":"/$2" }
	spec:
	  rules:
	  - http:
	      paths:
	      # use a commented property to pass the service path to DSS
	      # service-path: /my-subpath/to/the-service # __exposed_service_path__
	      - path: /my-subpath/to/the-service(/|$)(.*)
	        backend:
	          service:
	            name: svc-${executionId}
	            port:
	              number: 12000
	        pathType: ImplementationSpecific



Port forwarding
===============

This exposition doesn't create a Kubernetes service at all, and instead creates port forwarding processes from the DSS machine to the pods. The API service is then accessible locally on the the DSS machine (on 127.0.0.1). This exposition isn't intended to be used to make API services available outside the cluster.

