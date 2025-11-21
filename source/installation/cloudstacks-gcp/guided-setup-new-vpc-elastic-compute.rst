Guided setup 1: Deploy in a new VPC with Elastic Compute
########################################################

.. toctree::

.. contents::
    :local:

Description
===========

This guided setup allows you to install a full Dataiku Cloud Stacks for GCP, including the ability to run workloads on Elastic Compute clusters powered by Kubernetes (using GKE).

At the end of this walkthrough, you'll have:

* A fully-managed DSS design node, with either a public IP or a private one
* The ability to one-click create elastic compute clusters
* The elastic compute clusters running with public IPs (and no NAT gateway overhead)


Prerequisites
=============

You need to have, as an administrator, the permissions to create service accounts in the project and to grant IAM rights to these service accounts. Said service accounts need not have permission to grant IAM rights, they're only needed for the initial setup and required by the software during usage.

You need to have installed the `Cloud SDK <https://cloud.google.com/sdk/docs/install>` on a machine, and be able to run the `gcloud` command line assuming the same identity as in the console, and with the project set to the GCP project where the FM instance is to be deployed.

Steps
=====

Create a service account for your Fleet Manager instance
--------------------------------------------------------

* In your Google cloud controls, go to your project, and to the "IAM & admin" section

* In the "Service accounts" tab, click "Create service account"

* Enter a name for your service account

* Click on "Create and continue"

* In the "Grant this service account access to the project (optional)" part of the Service account creation screen, select and add the following roles: "Service account user", "Compute admin", "DNS administrator", "Cloud KMS Crypto operator"

* Click on "Continue" then "Done"

* In the list, take note of the "email" of the service account, this will be refered as ``fm-email``

* More permissions can be granted to the service account on the "IAM" tab, either by editing the service account line (with the pencil icon on the right) or by adding role assignments (with the "Add" button at the top)


Create a service account for your DSS instance
----------------------------------------------

* In your Google cloud controls, go to your project, and to the "IAM & admin" section

* In the "Service accounts" tab, click "Create service account"

* Enter a name for your service account

* Click on "Create and continue"

* In the "Grant this service account access to the project (optional)" part of the Service account creation screen, select and add the following roles: "Service account user", "Kubernetes engine admin", "Secret Manager Secret Accessor", "Compute viewer", "Artifact Registry Create-on-Push Writer" or "Artifact Registry administrator" if you want DSS to create the Artifact Registry repository for you.

* Click on "Continue" then "Done"

* In the list, take note of the "email" of the service account, this will be refered as ``dss-email``

* More permissions can be granted to the service account on the "IAM" tab, either by editing the service account line (with the pencil icon on the right) or by adding role assignments (with the "Add" button at the top)


Create a VPC to host the fleet manager
--------------------------------------

You'll need 2 CIDR for the network:

* one will be used for the network itself, and in fine for putting the VMs on the network. You can for example use "10.0.0.0/16". This CIDR will be referred as ``network-cidr``

* one will be used to allow internal routing on the network, between the VMs but also between secondary IP ranges that might be created in the network. This CIDR thus needs to be larger than ``network-cidr``, for example "10.0.0.0/8". This CIDR will be referred as ``internal-cidr``. Secondary ranges are used by GKE for pods and services (see `GKE doc <https://cloud.google.com/kubernetes-engine/docs/concepts/alias-ips>`_)


Then you can create a VPC network:

* In your Google cloud controls, go to your project, and to the "VPC network" section

* In the "VPC networks" tab, click "Create VPC network"

* Enter a name for the network; this will be referred as ``fm-network``

* In the "Subnets" section, make sure "Custom" is selected and create one subnet

* Enter a name for the subnet; this will be referred as ``fm-subnetwork``

* Enter a region for the subnet. The FM instance will be deployed in a zone of that region. This region will be referred as ``fm-region``

* For IPv4 range, enter the value chosen for ``network-cidr``

* Set "Private Google Access" to off

* Click "Create"

* Once the network is created, go to the "Firewall" tab

* Click "Create firewall rule"

* Set the name to "``fm-network``-external"

* Select :

    - "Network" -> ``fm-network``
    - "Direction" -> "Ingress"
    - "Action" -> "Allow"
    - "Targets" -> "All instances in the network"
    - "Source filter" -> "IPv4 ranges"
    - "Source IPv4 ranges" -> ``0.0.0.0/0``
    - "Protocols and ports" -> "Specified protocols and ports"

        * check "Tcp" and set the port to 22, 80, 443

* Click "Create"

* Again, click "Create firewall rule"

* Set the name to "``fm-network``-internal"

* Select :

    - "Network" -> ``fm-network``
    - "Direction" -> "Ingress"
    - "Action" -> "Allow"
    - "Targets" -> "All instances in the network"
    - "Source filter" -> "IPv4 ranges"
    - "Source IPv4 ranges" -> the value chosen for ``internal-cidr``
    - "Protocols and ports" -> "Allow all"

* Click "Create"


Deploy Fleet Manager
--------------------

.. _gcp_installation-infrastructure-manager:

Using Google Infrastructure Manager (recommended)
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

Infrastructure Manager is Google's replacement of Deployment Manager (more information about the decommission in :ref:`gcp_installation-deployment-manager`). It is based on Terraform.

* Fetch the Terraform file by running on the command line:

.. code-block::

    gsutil cp gs://dataiku-cloudstacks/templates/fleet-manager/14.2.2/fleet-manager-instance.tf .

* Create a `terraform.tfvars` file with inputs for the Terraform variables. Here is an example:

.. code-block::

    project_id = "<project-id>"
    region = "<region>"
    zone = "<zone>"
    deployment_name = "<deployment-name>"
    machine_type = "<machine-type>"
    network = "<network>"
    subnetwork = "<subnetwork>"
    username = "<fm-username>"
    password = "<fm-password>"
    service_account = "<fm-email>"
    allowed_cidr = "<allowed-cidr>"

where:
  - `project-id` is the ID of the project in Google cloud console
  - `region` is the GCP region where the resource should be deployed
  - `zone` is the GCP zone where the resource should be deployed (within the specified region)
  - `deployment-name` is a name for your deployment in the GCP Infrastructure Manager
  - `machine-type` is a GCE machine type like "n1-standard-4"
  - `network` is ``fm-network``
  - `subnetwork` is ``fm-subnetwork``
  - `fm-username` is a username for logging in to Fleet Manager
  - `fm-password` is a strong password for logging in to Fleet Manager
  - `fm-email` is the email of the service account for the FM instance that you created above
  - `allowed-cidr` is a CIDR of IP addresses that are allowed to connect to the FM instance

Additional options that can be used in the above parameters:
  - `ssh_key` is a RSA public key for SSH logging in to the underlying Fleet Manager virtual machine
  - `network_project_id`: project of the network (default is the current project). If different from the current project, `allowed_cidr` has no effect
  - `dss_service_account`: email of the service account DSS instances are to run as
  - `snapshot`: optional snapshot to create the instance with. Can be "projects/{project}/global/snapshots/{snapshot}" or "global/snapshots/{snapshot}"
  - `image`: optional image to create the instance with. Can be "projects/{project}/global/images/{image}" or "global/images/{image}"
  - `public_ip_address`: the public IP address to use for Fleet Manager
  - `ssl_mode`: the SSL mode for FM instance (``SELF_SIGNED`` if using a self-signed certificate, ``SECRET_MANAGER`` if using a certificate from the Certificate Manager)
  - `ssl_public_key`: the certificate in base 64
  - `ssl_gsm_secret_id`: the private key secret name
  - `kms_key_name`: the name of your encryption key in a KMS
  - `labels`: optional list of labels in key=value format to add to the resources that support them created by the deployment

.. code-block::

    labels = {
        key1 = "value1"
        key2 = "value2"
    }

* Make sure you have a service account that has the permissions necessary to apply the deployment. It needs to have at least edit permissions on the project resources, as well as role `roles/config.agent` (needed for Infrastructure Manager).

* Run the following command to apply an Infrastructure Manager deployment:

.. code-block::

    gcloud infra-manager deployments apply <deployment-name> \
        --location <region> \
        --service-account projects/<project-id>/serviceAccounts/<service-account-email> \
        --local-source <terraform-folder>

where:
  - `deployment-name` is the name of the deployment object in Infrastructure Manager
  - `region` is the GCP region where the resource should be deployed
  - `service-account-email` is the email of the GCP service account that will run the operation
  - `terraform-folder` is the folder containing both the Terraform template and the `.tfvars` input file

* Wait for your deployment to complete

In order to retrieve the address at which your Cloud Stacks Fleet Manager is deployed, run

.. code-block::

    gcloud infra-manager deployments export-statefile <deployment-name> \
        --location <region> \
        --file=state

where:
  - `deployment-name` is the name of the deployment object in Infrastructure Manager
  - `region` is the GCP region where the resource should be deployed

The deployment state will be stored in file `state.tfstate` and the IP can be found in `outputs.fm_server_ip` field.

.. _gcp_installation-deployment-manager:

Using Google Deployment manager (deprecated)
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

.. warning::

    Deployment Manager will be decommissioned by Google soon, please prefer the alternatives described above. Reference: https://cloud.google.com/deployment-manager/docs/deprecations

* Fetch the template files by running on the command line

.. _gcp-cloudstacks-fm-template:

.. code-block::

    gsutil cp gs://dataiku-cloudstacks/templates/fleet-manager/14.2.2/fleet-manager-instance.jinja .
    gsutil cp gs://dataiku-cloudstacks/templates/fleet-manager/14.2.2/fleet-manager-instance.jinja.schema .

* Start the deployment by running on the command line

..  code-block::

    gcloud deployment-manager deployments create <deployment-name> --template fleet-manager-instance.jinja --properties zone:<zone>,machineType:<machine-type>,network:<network>,subnetwork:<subnetwork>,serviceAccount:<fm-email>,allowedCIDR:<allowed-cidr>,username:<fm-username>,password:<fm-password>,sshKey:"<fm-authorized-key>",labels:key1=value1;key2=value2

where:
  - `deployment-name` is a name for your deployment in the GCP Deployment Manager
  - `zone` is the GCP zone where the resource should be deployed
  - `machine-type` is a GCE machine type like "n1-standard-4"
  - `network` is ``fm-network``
  - `subnetwork` is ``fm-subnetwork``
  - `fm-email` is the email of the service account for the FM instance that you created above
  - `allowed-cidr` is a CIDR of IP addresses that are allowed to connect to the FM instance
  - `fm-username` is a username for logging in to Fleet Manager
  - `fm-password` is a strong password for logging in to Fleet Manager
  - `fm-authorized-key` is a RSA public key for SSH logging in to the underlying Fleet Manager virtual machine

Additional options can be used in the above command:
  - `networkProject`: project of the network (default is the current project). If different from the current project, `allowedCIDR` has no effect
  - `privateIpAddress`: optional static private IP address for Fleet Manager
  - `publicIpAddress`: optional static public IP address for Fleet Manager. Specify an unused static external IP address available in the project. If you specify a static external IP address, it must live in the same region as the zone of the instance
  - `dssServiceAccount`: email of the service account the DSS instances are to run as
  - `snapshot`: optional snapshot to create the instance with. Can be "projects/{project}/global/snapshots/{snapshot}" or "global/snapshots/{snapshot}"
  - `labels`: optional semicolon-separated list of labels in key=value format to add to the resources that support them created by the deployment (e.g. key1=value1;key2=value2)

* Wait for your deployment to complete

The deployment command will output the IP of the instance it spawned. This is the address at which your Cloud Stacks Fleet manager is deployed. Open a new tab to this address and wait for the login screen to appear.

.. note::

    If re-deploying, or deploying after failure on a previous deployment of the template, you can also use ``gcloud deployment-manager deployments update ...`` instead of ``gcloud deployment-manager deployments create ...``

The command-line version of the ``gcloud deployment-manager deployments create ...`` command can also be used with a config file. For example a ``config.yaml`` file with:

.. code-block::

    imports:
    - path: fleet-manager-instance.jinja
      name: fleet-manager-instance
    resources:
      - name: fleet-manager-instance
        type: fleet-manager-instance.jinja
        properties:
            zone: <zone>
            machineType: <machine-type>
            network: <network>
            subnetwork: <subnetwork>
            serviceAccount: <fm-email>
            allowedCIDR:< allowed-cidr>
            username: <fm-username>
            password: <fm-password>
            sshKey: "<fm-authorized-key>"
            labels: key1=value1;key2=value2

yields the same deployment as the command above with

.. code-block::

    gcloud deployment-manager deployments create <deployment-name> --config=config.yaml



Start your first DSS
--------------------

* Log into Fleet Manager with the login and the password you previously entered

* In "Cloud Setup", click on "Edit", set "License mode" to "Manually entered", click on "Enter license" and enter your Dataiku license. Click on "Done" then on "Save"

* Refresh the page in your browser

* In "Fleet Blueprints", click on "Deploy Elastic Design"

* Give a name to your new fleet, this will be refered as ``fleet-name``

* In "Instance service account", enter the ``dss-email``

* Click on "Deploy"

* Go to "Virtual Networks", select the "Virtual network for fleet ``fleet name``"

* In the settings, in "Network tags", put "tag-<deployment-name>", where <deployment-name> is the name used for the deployment in the previous commands, and Save

* Go to "Instances > All", click on the design node

* Click "Provision"

* Wait for your DSS instance to be ready

* Click on the **Retrieve** button under "Retrieve password" and write down the password

* Click on "Go to DSS"

* Login with "admin" as the login, and the password you just retrieved

You can now start using DSS

(Optional) Start your first Elastic compute cluster
---------------------------------------------------

Deploy your Elastic Compute cluster
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

* In DSS, go to Administration > Clusters

* Click on "Create GKE cluster", give it a name

* In "Connection", check it is set to "Manually defined"

* In section "Networking", check that "Inherit DSS host settings"  is checked.

* In section "Networking", check that "Make cluster VPC-native"  is checked, and fill "Pod IP range" and "Service IP range". Both ranges should be within the `internal-cidr` used when deploying the FM template, and non-overlapping with `network-cidr`. If `network-cidr` is `x.y.0.0/16` and `internal-cidr` is `x.0.0.0/8` then you can leave GKE to create automatically the ranges.

* In "Cluster Nodes", Click on "+ Add a preset"

* Update "Machine type" and "Disk size" as you see fit

* Tick the "Enable nodes autoscaling" box

* In "Advanced options", set "Service account type" to "Same as DSS host"

* Click on "Start"

* Wait for your cluster to be available

* In Settings, go to "Containerized execution", and in "Default cluster", select the cluster you just created.

* In the "gke-default" configuration, adjust the "Image registry url" if needed

* Click on "Save" then "Push base images". When finished, click on "(Re)Install Jupyter kernels".

* In a project, you can now use containerized execution for any activity, using the containerized config you created
