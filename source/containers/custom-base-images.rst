Customization of base images
#############################

.. contents::
	:local:

.. warning::

	This requires knowledge of Docker concepts and skills in creating custom Dockerfiles.

When building the base image with

.. code-block:: bash

	./bin/dssadmin build-base-image --type container-exec

a default base image is created with:

* Python 3.9, also Python 3.10 if DSS uses Python 3.10
* R 4
* No CUDA support

This can be customized with options to enable or disable additional language versions, eg ``--with-py311 --without-r``.

Run ``./bin/dssadmin build-base-image --help`` for details.

.. |base-image-type| replace:: container-exec

.. include:: /containers/_base-image-cuda-support.txt

Multiple base images
=====================

If you don't use the ``--tag`` flag, DSS builds a base image with this naming scheme:

.. code-block:: bash

	dku-exec-base-DSS_INSTALL_ID : dss-DSS_VERSION

Where

* DSS_INSTALL_ID is the identifier of the DSS installation, found in the ``install.ini`` file.
* DSS_VERSION is the version of DSS.

If you don't specify anything in the "base image" field of the DSS containerized execution configuration, this tag will automatically be used.

You can build other base images by appending the ``--tag IMAGE_NAME:IMAGE_VERSION`` flag to the ``./bin/dssadmin build-base-image --type container-exec`` command.

Setting a proxy
================

You can set the proxy to use to build with ``--http-proxy``  and ``--no-proxy`` to set the ``http_proxy`` and ``no_proxy`` environment variables.

Adding system packages
=======================

There are cases where you would want to install additional system packages, generally because they are required by your code environments.

For that, add ``--system-packages package1,package2,package3``

Add a Dockerfile fragment
=============================

You may want to add custom Dockerfile commands. For that, use ``--dockerfile-prepend PATH_TO_FILE`` or ``--dockerfile-append PATH_TO_FILE``.

The prepended Dockerfile is added just after the FROM. The appended Dockerfile is added at the very end of the Dockerfile.

To add a file to the build context, to make the file available to use in Dockerfile commands added via fragment, use ``--copy-to-buildenv absolute/path/file.name file.name``.

Completely custom Dockerfile
=============================

For cases not covered, the generic process would be:

* Build a base image with the regular DSS mechanisms.
* Write a custom Dockerfile that starts from the built base image, and add the required package.
* Build this custom Dockerfile, and output a custom tag.
* Enter this custom tag in the DSS containerized execution configuration.

.. warning::

	After each upgrade of DSS, you must rebuild all base images, including custom ones.
