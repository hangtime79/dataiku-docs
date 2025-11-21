Concepts
########

.. contents::
	:local:


What is a Code Studio
======================

A Code Studio is a personal space for running a web-based IDE, within DSS, and optionally one or several web applications.

Code Studios run in Kubernetes, and require setup of :doc:`/containers/index`.

Some of the capabilities made possible by Code Studios include:

* Editing and debugging Python recipes in Visual Studio Code
* Debugging Python code in JupyterLab
* Developing custom web applications using the Streamlit framework
* Editing and debugging R recipes in RStudio Server

Within each instance of a Code Studio, you have full access to the terminal, can install any package, perform any action, save your IDE preferences, ...

Each Code Studio can be started and stopped.

Each Code Studio is a separate container and has its separate filesystem. It cannot access the DSS host filesystem.

.. note::

	In Dataiku Cloud, a space-admin needs to activate the feature « Code-Studio » in the Launchpad (extension tab > add an extension). The feature will be ready to use without needing any additional requirements.

Code Studio templates
======================

Before you can run a Code Studio, the DSS administrator must set up a *Code Studio template*.

Each template provides a specific development environment and optional additional dependencies.

For example, you could have:

* one template providing RStudio Server
* another template containing the Visual Studio Code IDE + the streamlit framework for developing advanced visualizations

Users can then, from these templates, spawn personal instances of the development environments, called Code Studios. To follow our example, these Code Studios can then be used to edit an existing R recipe in DSS, or to develop a streamlit webapp using Visual Studio Code.

The template consists of *blocks* that define what will be available in the Code Studio.

Technical details
==================

At its core, a Code Studio is a Kubernetes pod running an HTTP server in a Kubernetes cluster. DSS starts it and shuttles files between the DSS instance and the container inside the pod, then forwards requests on the DSS UI to the HTTP server.


To start and connect to a pod in a Kubernetes cluster, DSS must:

* prepare container images
* prepare Kubernetes resource definitions to start a pod in the cluster
* identify ports on which the pod serves its app

All this is defined within the Code Studio template. Additionally, the template defines which files from the DSS filesystem are shared with the container in the cluster.

Once a Code Studio template has been prepared and is available to some users, they can start creating Code Studios to run the application(s) defined in that template, and access it via DSS. Here, "application" is something served by an HTTP server, and the runtime is hosting the HTTP server. Each Code Studio spawns some Kubernetes resources, typically a deployment, leading to a pod somewhere in the cluster running the application(s). DSS then synchronizes the files from the DSS filesystem to the container in the pod, as defined in the template, and starts the web server in the container.

Once running, the user can connect to all applications (that is, their HTTP servers) running in the container, use them as appropriate to edit files or perform analyses, and finally synchronize back modified files from the container to the DSS filesystem.
