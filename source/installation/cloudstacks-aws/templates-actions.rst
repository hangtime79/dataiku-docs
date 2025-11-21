Instance templates and setup actions
####################################

.. contents::
	:local:

Instance template represent common configuration for instances, reusable across several instances. It is required to use an instance template to launch an instance. Instances stay linked to their instance template for their whole lifecycle.

What is configured through the instance templates includes, but is not limited to:

* Identities able to SSH to the instance
* Cloud credentials for the managed DSS
* Installation of additional dependencies and resources
* Pre-baked and custom configurations for DSS

To create, edit and delete templates, head to the *Instance templates* in the left menu of FM. The following document explains each section of the configuration.

SSH keypair
===========

Use this field to select which AWS EC2 keypair will be deployed on the instance. This is useful for admins to connect to the machine with SSH. This field is optional.

This key will be available on the ``ec2-user`` account (``centos`` for DSS instances prior version 12), i.e. you will be able to login as ``ec2-user@DSS.HOST.IP``


AWS credentials
===============

In most cases, your DSS instances will require AWS credentials in order to operate. These credentials will be used notably to integrate with ECR and EKS. They can also be used (optionally) for S3 connectivity.

The recommended way to offer AWS credentials to DSS instance is the use of an IAM instance profile. You can create a role, and put its instance profile ARN as the "runtime instance profile ARN" field.

Keep "restrict access to metadata server" enabled so that DSS end-users cannot access these credentials.

Atypical options
----------------

There may be some cases where you want setup to have additional permissions, notably being able to retrieve secrets from ASM, or perform other tasks that might require permissions useful for startup only (see :ref:`setup actions <aws_cloudstacks-actions-setup>`).

If that's needed, you can add a "Startup instance profile ARN" that will only be available during startup and that will be replaced by the "Runtime instance profile ARN" once startup is complete.

Alternatively to IAM instance profile, you can also use a keypair that will be given to the DSS service account.

The AWS Secret Access Key can be stored in ASM (in which case the **Startup instance profile ARN** must be able to read it) or encrypted and stored by FM (in which case the **Startup instance profile ARN** must be able to user the CMK to decrypt it).

.. _aws_cloudstacks-actions-setup:

Setup actions
=============

Setup actions are configuration steps ran by the :ref:`agent <cloudstacks-concept-agent>`. As a user, you create a list a setup actions you wish to see executed on the machine.

.. include:: /installation/setup-actions/_install_system_packages.rst

Add authorized SSH key
----------------------

This setup action ensures the SSH public key passed as a parameter is present in `~/.ssh/authorized_keys` file of the default admin account. The default admin is the `ec2-user` user with currently provided images.

.. include:: /installation/setup-actions/_set_advanced_security.rst
.. include:: /installation/setup-actions/_install_a_jdbc_driver.rst
.. include:: /installation/setup-actions/_run_ansible_tasks.rst
.. include:: /installation/setup-actions/_setup_kubernetes_and_spark.rst
.. include:: /installation/setup-actions/_add_environment_variables.rst
.. include:: /installation/setup-actions/_add_properties.rst
.. include:: /installation/setup-actions/_add_ssh_key.rst

Setup proxy
-----------

This setup action enables to configure a proxy in front of DSS.

The default value for the `NO_PROXY` variable is: `localhost,127.0.0.1,169.254.169.254`.

`169.254.169.254` is the IP used by AWS to host the metadata service.

.. include:: /installation/setup-actions/_add_certificate_authority.rst
.. include:: /installation/setup-actions/_install_code_env_with_visualml_preset.rst
