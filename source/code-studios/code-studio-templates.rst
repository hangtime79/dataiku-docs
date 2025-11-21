Preparing Code Studio templates
###############################

Code Studio templates are prepared by the DSS administrator, in the Administration section of DSS. Permissions to use the templates can then be granted to groups.

.. contents::
	:local:

Building blocks
===============

Templates are built from blocks, each adding some configuration to the Code Studios. The blocks are applied sequentially, so blocks can rely on the modifications defined in previous blocks.

Standard blocks
----------------

Visual Studio Code
%%%%%%%%%%%%%%%%%%%

This block adds the VS Code IDE in the Code Studio. Each code env added by an "Add code environment" block is added to VS Code as a debug configuration and is available from the list of interpreters.

It is not usually needed to change any setting of this block.

JupyterLab server
%%%%%%%%%%%%%%%%%%

This block adds the JupyterLab IDE in the Code Studio. Each code env added by a "Add code environment" block is added as a kernel in JupyterLab.

It is not usually needed to change any setting of this block.


RStudio
%%%%%%%%

This block adds the RStudio Server IDE in the Code Studio.

It is not usually needed to change any setting of this block.

Streamlit
%%%%%%%%%

This block adds the Streamlit application building framework in the Code Studio and adds an entry point that runs the application. This allows you to both edit and run the application directly from the Code Studio.

By default, Streamlit use its own code env with necessary dependencies, but you can also choose an existing code environment (which must include the streamlit dependency).

The Streamlit application is automatically bootstrapped and can be edited directly from the "Code Studio Versioned Files", in the `streamlit/app.py` file.


Gradio
%%%%%%

This block adds the Gradio application building framework in the Code Studio and adds an entry point that runs the application. This allows you to both edit and run the application directly from the Code Studio.

By default, Gradio use its own code env with necessary dependencies, but you can also choose an existing code environment (which must include the gradio dependency).

The Gradio application is automatically bootstrapped and can be edited directly from the "Code Studio Versioned Files", in the `gradio/app.py` file.


Voila
%%%%%%

This block adds the Voilà framework in the Code Studio and adds an entry point that runs the application. This allows you to both edit and run the application directly from the Code Studio.

By default, Voilà use its own code env with necessary dependencies, but you can also choose an existing code environment (which must include the voila dependency).

You choose from multiple flavors:

* ``voila + DSS - compatible with Jupyterlab`` let you used Voilà within JupyterLab.
* ``voila-vuetify + DSS`` setup Voilà with the Dataiku Python client and Vuetify.
* ``voila-material + DSS`` setup Voilà with the Dataiku Python client and Material.
* ``voila-gridstack + DSS`` setup Voilà with the Dataiku Python client and Gridstack.
* ``latest voila version + DSS`` setup the latest Voilà version with the Dataiku Python client.
* ``Custom voila version`` let you setup a code environment including Voilà by yourself (advanced).


The Voilà application is automatically bootstrapped and can be edited directly from the "Code Studio Versioned Files", in the `voila/app.ipynb` file.


.. _block_code_studio_code_env:

Add a code environment
%%%%%%%%%%%%%%%%%%%%%%%

This block installs the specified code environment in the designated location in the container.

* If your template contains JupyterLab, the code environment is also automatically registered as a Kernel.
* If your template contains VS Code, the code environment is also automatically registered as a run config (debug panel), and as an interpreter (bottom right menu) in VS Code


Advanced blocks
----------------


.. _block_append_to_dockerfile:

Append to DockerFile
%%%%%%%%%%%%%%%%%%%%%

A Code Studio template is primarily defined by the image that its container runs.

This block allows you to add arbitrary Dockerfile statements to the image. Each instance of this block appends to the Dockerfile of the image that is built.

The image starts from the DSS base image.

| In the DockerFile section, you can refer to the path of template resources with ``__TEMPLATE_RESOURCES__``.
| eg: ``COPY __TEMPLATE_RESOURCES__/my-file /home/dataiku/workspace/my-file``.

| Resources listed in the block are copied to the Docker build context, next to the Dockerfile.
| You can use ``${dku.install.dir}`` and ``${dip.home}`` to point to the DSS installation directory and data directory respectively. You can also use ``${template.resources}`` to point to the resources uploaded on this template.
| eg: ``${template.resources}/my-folder/my-file`` → ``/home/dataiku/workspace/my-file``.


.. _block_add_entrypoint:

Add an entry point
%%%%%%%%%%%%%%%%%%

The actual entry point of the container is defined by DSS to be a technical "runner.py" script that's part of the base DSS image. To start actual HTTP servers in the container, the template must define at least one entry point that this technical script will launch.
Each entry point can also declare a port on which it's expected to be running an HTTP server. That HTTP server is then made available in the DSS UI. To forward the HTTP communication to the DSS UI:

- make sure **Expose HTML service** is checked. If left unchecked, the HTTP server is accessible by requesting its URL directly but not shown in the UI. The URL is built as `http[s]://studio-host:port/dip/code-studios/<project-key>/<code-studio-id>/<exposed-port>/`
- whether the HTTP server is launched when using this template in a Webapp
- specify a **label** to use on tabs in the Code Studio's "View"
- specify a **proxied subpath** that is given to a ``proxy_pass`` in an Nginx configuration. What to use depends on the capabilities of the HTTP server in the Code Studio, and in particular whether it's able to handle a path prefix. A value of ``/`` works for most cases, but when the server can't handle a path prefix, you should use ``$request_uri`` and force the server in the Code Studio to use a fixed prefix. DSS sets a ``$DKU_CODE_STUDIO_BROWSER_PATH_<exposed-port>`` variable in the Code Studio that the server entry point can use to set its path prefix.


Add custom action
%%%%%%%%%%%%%%%%%%

While the Code Studio is up, some predefined actions can be triggered inside the container by the user, from the Code Studio's "Actions" tab. Each action is a command line.


.. _block_add_starter_files:

Add starter files
%%%%%%%%%%%%%%%%%%

When a Code Studio is created from the template, the template writer can add predefined files inside the code-studio-specific file zones and user-specific file zones on the DSS server's filesystem. This can for example be used to provide an initial working version of code for a webapp. The files are only added upon creating the Code Studio, not when (re)starting it.

| You can use ``${dku.install.dir}`` and ``${dip.home}`` to point to the DSS installation directory and data directory respectively. You can also use ``${template.resources}`` to point to the resources uploaded in this template.
| eg: ``${template.resources}/my-folder/my-file`` → ``/home/dataiku/workspace/my-file``.


NGINX
%%%%%

.. note::

	This block is not available on Dataiku Cloud.

This block basically allows you to have an HTTP access on your "zones" folders.
With it you can easily make simple webapps.
You can also setup a proxy on a "manually" installed framework for example.

Special blocks
----------------

File synchronization
%%%%%%%%%%%%%%%%%%%%%

This special block defines which files are synchronized with the Code Studio and where. See :ref:`synchronized_files` for more details about the different file locations.


Each synchronization definition consists of:

* a "zone" of the DSS server's filesystem
* optionally a sub-folder of that zone
* a target location in the container.

A synchronization can be made one-way by toggling the arrow; if one-way, then files are copied from the DSS server's filesystem to the Code Studio, but not the other way around. The block also sports a list of exclusions to define which files on the container are excluded from synchronization. The exclusions follow the syntax used by `gitignore <https://git-scm.com/docs/gitignore>`_ (minus the ``!`` negation)


Kubernetes parameters
%%%%%%%%%%%%%%%%%%%%%%

This special block controls advanced settings.

The container in which the Code Studio actually runs is spawned as a pod in a Kubernetes deployment (single replica). In order to have a proper deployment, a functioning readiness probe is needed, and that is the main purpose of this block. The simplest is to activate TCP probing, and DSS will set the deployment to probe on the first exposed port of the container. (see :ref:`readiness_probes`)

This block also specifies to DSS which URL to use in order to probe the readiness of the HTTP server inside the container. This probing is independent of the one done by Kubernetes to find out whether the deployment rollout is finished. If using the JupyterLab / RStudio / VisualCode blocks, this field is not necessary, because these blocks will automatically adjust the readiness probe URL.

Finally, the block allows for defining additional exposed ports. However, these ports should preferably be defined from the :ref:`block_add_entrypoint` block.

Advanced template building
============================

Template resources
-------------------

You can attach files to this template by uploading them in the "Resources" tab.
These files can be used in the :ref:`block_append_to_dockerfile` or :ref:`block_add_starter_files`.


Environment variables in the pod
----------------------------------

The pod running the Code Studio receives some parameters using environment variables:

- ``DKU_CODE_STUDIO_BROWSER_PATH`` : the path prefix used by DSS in front of the Code Studio in the UI. Its value is defined by DSS, and is currently ``/code-studios/<project_key>/<code_studio_id>`` in a code studio.
- ``DKU_CODE_STUDIO_BROWSER_PATH_{port}`` : the specific path prefix used for a given exposed port (starts with ``DKU_CODE_STUDIO_BROWSER_PATH``). Its value is ``/code-studios/<project_key>/<code_studio_id>/<port_number>``
- ``K8S_NODE_NAME``, ``K8S_POD_NAME``, ``K8S_POD_NAMESPACE``, ``K8S_POD_ID`` : exposed from Kubernetes via the `downward API <https://kubernetes.io/docs/tasks/inject-data-application/environment-variable-expose-pod-information/#the-downward-api>`_


These variables are also defined for code studios published as webapps, but:

- the values of the ``DKU_CODE_STUDIO_BROWSER_PATH*`` variables is different, and corresponds to the usual backend path prefixes for webapps, like ``/web-apps-backends/<project_key>/<web_app_id>...``
- the variables' values can contain other variables. A typical case is a webapp that's exposed using the default port forward exposition, where ``DKU_CODE_STUDIO_BROWSER_PATH`` is valued ``/web-apps-backends/<project_key>/<web_app_id>_${K8S_POD_NAME}`` (so you have to perform the replacement of ``K8S_POD_NAME`` in the pod itself)

.. _readiness_probes:

Readiness probes
-----------------

Code Studios run in pods in the cluster, and these pods are spawned by (Kubernetes) deployments. Deployments are typically started, and "rolled out" by the cluster. In order to do a proper rollout, Kubernetes needs to probe the pods to determine whether they're ready. If pods cannot be flagged as ready, then rollout fails and ultimately the Code Studio shuts down. This flagging as ready is the work of `readiness probes <https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/>`_. Additionally, when the Code Studio is used as a webapp, DSS also probes the Code Studio over HTTP, to decide whether it's ready to be shown in the UI.

Kubernetes can do readiness probing on Code Studio with 2 mechanisms:

- TCP probing (= check if some port is used by a server on the pod). Usually more reliable.
- HTTP probing (= check if some request to the pod gets a response with a non-failure status).

.. warning::
    HTTP probing is rather unreliable when using Code Studio as a WebApp. Prefer TCP probing in that case.

DSS only probes readiness through HTTP requests.

When writing a Code Studio template and not using the default JupyterLab/RStudio/VSCode blocks, it is necessary to fill a working readiness probe URL. It is also advised to check **TCP probing**. If the HTTP server inside the Code Studio needs to work with a path prefix, the readiness probe should include it by using ``${baseUrl}``.
