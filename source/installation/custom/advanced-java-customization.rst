Advanced Java runtime configuration
######################################

.. contents::
	:local:

Java requirements
=================

DSS is a Java application, and requires a compatible Java environment to run. Supported versions are `OpenJDK <http://openjdk.java.net>`_, Amazon Corretto and `Oracle JDK <https://www.oracle.com/technetwork/java/javase/downloads/index.html>`_, version 17

Unless instructed otherwise (see :ref:`below <java.custom_jre>`) the DSS installer will automatically look for a suitable version of Java
in standard locations. If none is found, it will install an appropriate OpenJDK package as part of its dependency installation phase.

.. note::

	Starting with DSS 14, Java 8 and Java 11 are no longer supported.

	While the Java Runtime Environment (JRE) is technically sufficient for DSS to run, it is recommended to install the
	full Java Development Kit (JDK) as this includes additional tools for diagnosing performance and other technical issues.
	Dataiku support may require you to install the full JDK to investigate some cases.

.. _java.custom_jre:

Choosing the JVM
----------------

You can force Data Science Studio to use a specific version of Java (for example, when there are several versions installed on the
server, or when you manually installed Java in a non-standard place) by setting the **JAVA_HOME** environment variable
while running the DSS installer script. This variable should point to the installation directory of the Java runtime to use. For example:

.. code-block:: bash

    $ JAVA_HOME=/usr/lib/jvm/java-17-openjdk dataiku-dss-VERSION/installer.sh <INSTALLER_OPTIONS>

Note that the installer script stores this value in the file ``DSS_DATADIR/bin/env-default.sh`` (in variable ``DKUJAVABIN``), so this environment variable is only needed
at installation time. It must be provided for all subsequent DSS updates however, unless one wishes DSS to revert to the automatically-detected
version of Java.

Switching the JVM
-----------------

You can switch an existing DSS instance to an different version of Java by rerunning the installer
in update mode with a new value for **JAVA_HOME**, as follows:

.. code-block:: bash

	# Stop DSS
	$ DSS_DATADIR/bin/dss stop

	# Switch this DSS instance to a different Java runtime
	$ JAVA_HOME=/PATH/TO/NEW/java dataiku-dss-VERSION/installer.sh -d DSS_DATADIR -u

	# Restart DSS
	$ DSS_DATADIR/bin/dss start


Customizing Java runtime options
===================================

The DSS installer generates a default set of runtime options for the DSS Java processes, based on the Java version in use and the
memory size of the hosting server. These options can be customized if needed.

.. _java.processes.definition:

The different Java processes
----------------------------

DSS is made up of 4 different kinds of Java processes:

* The "backend" is the main server, which handles all interaction with users, the configuration, and the visual data preparation. There is only one backend.
* The "jek" is a process which runs the jobs (ie, what happens when you use "Build"). There are multiple jeks (one per running job)
* The "fek" handles long-running background tasks. It is also responsible for building the data samples. There are multiple feks (one per running background task)
* The "hproxy" handles interactions with Hive. There is only one hproxy.

For the API node:

* The "apimain" is the main server.

For the Govern node:

* The "governserver" is the main server.

What can be customized
----------------------

All Java options of these 6 kinds of processes can be customized.

For each of these, DSS provides an easy way to:

* configure the amount of memory allocated to each process (Java "-Xmx")
* add custom options

These customizations can be done by editing the :ref:`install.ini <install.ini>` file.

More advanced customization (taking precedence over default DSS options) can be done via environment files.

.. _java.memory.tuning:

Customizing maximum memory size (xmx)
-------------------------------------

Most often, you will want to customize the amount of memory ("xmx") variable, which is the maximum memory allocated to the Java process.

Xmx is configured by setting the ``<processtype>.xmx`` setting in the ``javaopts`` section of the install.ini file (where ``<processtype>`` is one of
backend, jek, fek or hproxy).

The installer sets Xmx to a default value between 2 and 6 GB, depending on the memory size of the host. This might not be enough for DSS instances
with a large number of users. If that amount of memory is not sufficient, the DSS backend may crash, and all users would get disconnected until
it automatically restarts.

Example: Set Xmx of backend to 8g
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

* Go to the DSS data directory

.. note::

	On macOS, the ``DSS_DATADIR`` is always: ``$HOME/Library/DataScienceStudio/dss_home``

* Stop DSS

	.. code-block:: bash

		./bin/dss stop

* Edit the install.ini file
* If it does not exist, add a ``[javaopts]`` section

* Add a line: ``backend.xmx = 8g``

* Regenerate the runtime config:

	.. code-block:: bash

		./bin/dssadmin regenerate-config

* Start DSS

	.. code-block:: bash

		./bin/dss start

Example install.ini
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

Here is an example of an install.ini file that configures the Xmx for backend and jek:

.. code-block:: bash

	[javaopts]
	backend.xmx = 8g
	jek.xmx = 4g

Memory amounts can be suffixed with "m" or "g" for megabytes and gigabytes


.. _java.additional.options:

Adding additional Java options
------------------------------

You can add arbitrary options to the DSS Java processes. Use the same procedure as above, with ``<processtype>.additional.opts``
directives:

.. code-block:: bash

	[javaopts]
	backend.additional.opts = -Dmy.option=value


Advanced customization
------------------------

The full Java runtime options can be configured by setting environment variables in the ``DSS_DATADIR/bin/env-site.sh`` file in the Data Science Studio data directory.

.. warning::

	You should only use this section if you could not obtain the desired set of options using the options above.

The default runtime options are stored in several environment variables:

	* DKU_BACKEND_JAVA_OPTS
	* DKU_JEK_JAVA_OPTS
	* DKU_FEK_JAVA_OPTS
	* DKU_HPROXY_JAVA_OPTS
	* DKU_APIMAIN_JAVA_OPTS
	* DKU_GOVERNSERVER_JAVA_OPTS

The default values for these files (computed from ``DSS_DATADIR/install.ini``) are stored in ``DSS_DATADIR/bin/env-default.sh``.

.. warning::

	Do not modify ``DSS_DATADIR/bin/env-default.sh``, it would get overwritten at the next Data Science Studio upgrade and after each call to ``./bin/dssadmin regenerate-config`` or ``./bin/governadmin regenerate-config`` for the Govern node

To configure these options:

* Stop DSS

	.. code-block:: bash

		./bin/dss stop

* Open the ``DSS_DATADIR/bin/env-default.sh`` file
* Copy the line you want to change. They look like ``export DKU_BACKEND_JAVA_OPTS``, ``export DKU_JEK_JAVA_OPTS``, ...
* Open the ``DSS_DATADIR/bin/env-site.sh`` file
* Paste the line and modify it to your needs

* Start DSS

	.. code-block:: bash

		./bin/dss start


.. _java.ssl.truststore:

Adding SSL certificates to the Java truststore
==============================================

There are a number of configurations where DSS needs to connect to external resources using secure network connections (SSL / TLS). This
includes (but is not limited to):

* connecting to a secure LDAP server
* connecting to Hadoop components (Hive, Impala) over SSL-based connections
* connecting to SQL databases, MongoDB, Cassandra, ... over secure connections

In all these cases, the Java runtime used by DSS needs to be able to verify the identity of the remote server, by checking that its certificate
is derived from a trusted certification authority. The JVM comes with a default list of well-known Internet-based certification authorities,
which normally covers all legitimate publicly-accessible Internet resources. However, resources internal to your organization are typically
certified by private certification authorities, or by standalone (self-signed) certificates. It is then necessary to add additional certificates
to the trusted list of the JVM used by DSS (a.k.a. truststore).

You should refer to the documentation of your JVM and/or Linux distribution for the precise procedure for this. In most cases, you can use one of
the following options:

Add a local certificate to the global JVM truststore
----------------------------------------------------

You will need write access to the Java installation for this (that would be root access for the typical case where the JVM has been installed
through a package manager).

* check which JVM is used by DSS by looking for variable ``DKUJAVABIN`` in file ``DSS_DATADIR/bin/env-default.sh``
* locate the physical installation directory of this JVM with : ``readlink -f /PATH/TO/java``. This should resolve to ``JAVA_HOME/bin/java``  where ``JAVA_HOME`` is the installation directory for this JVM.
* locate the default truststore file, at ``JAVA_HOME/lib/security/cacerts``
* prepare the certificate(s) to add, in one of the supported file formats (binary- or base64-encoded DER, typically named .pem, .cer, .crt,
  or .der, or PKCS#7 certificate chain, typically named .p7b, or .p7c)
* import your certificate in the JVM trustore with ``keytool`` (the certificate store management tool, shipped with the JVM).
  This command prompts for the trustore password, which by default is ``changeit`` on Oracle and OpenJDK distributions.

  .. code-block:: bash

  	keytool -import [-alias FRIENDLY_NAME] -keystore /PATH/TO/cacerts -file /PATH/TO/CERT_TO_IMPORT

  You may need to first make this file writable with chmod, if it is write-protected.

  You can check that the import was successful by listing the new truststore contents:

  .. code-block:: bash

  	keytool -list -keystore /PATH/TO/cacerts

You need to restart DSS after this operation.

.. warning::

	This operation may need to be redone after an update of the JVM, or of the global system-wide certificate trust list.

.. note::

	Instead of directly modifying the default trustore at ``JAVA_HOME/lib/security/cacerts``, you can duplicate it to a file
	named ``jssecacerts`` in the same directory, and update this file instead. When this file exists, it overrides the default one,
	which lets you preserve the original, distribution-provided version.

	For full reference to the management of SSL certificate trust stores, refer to the documentation of your Java runtime.
	For Oracle JRE, you can refer to:

	* https://docs.oracle.com/en/java/javase/17/security/java-secure-socket-extension-jsse-reference-guide.html#GUID-7D9F43B8-AABF-4C5B-93E6-3AFB18B66150
	* https://docs.oracle.com/en/java/javase/17/tools/keytool.html


Add a local certificate to the system-wide certificate trust list
-----------------------------------------------------------------

You need to be root for this operation.

Most Unix distributions maintain and distribute a system-wide trusted certificate list, which is in turn used by the various subsystems which need
it, including all distribution-installed JVMs. Following distributions-specific procedures to add custom certificates to this list ensures that
these additions are not lost upon system or JVM updates, and are available to other subsystems as well (eg command-line tools).

On RedHat-compatible systems, the global trustore is built with ``update-ca-trust(8)`` as follows (refer to the manpage for details):

* (as root) add any local certificates to trust in directory ``/etc/pki/ca-trust/source/anchors/``
* (as root) run : ``update-ca-trust extract``
* optionally, check with: ``keytool -list -keystore JAVA_HOME/lib/security/cacerts -storepass changeit``

On Debian / Ubuntu systems, the global truststore is built with ``update-ca-certificates(8)`` as follows (refer to the manpage for details):

* (as root) add any local certificates to trust in directory ``/usr/local/share/ca-certificates`` (or a subdirectory of it), as a file
  with extension ".crt"
* (as root) run : ``update-ca-certificates``
* optionally, check with: ``keytool -list -keystore JAVA_HOME/lib/security/cacerts -storepass changeit``

You need to restart DSS after this operation.


Run DSS with a private truststore
---------------------------------

If you lack administrative access required to update the global truststore (system-wide, or JVM default), you can copy the global trustore to a
private location, add your custom certificates to it, and direct DSS to use it instead of the default trustore.

* Using the same steps as the first solution above, locate the default JVM truststore at ``JAVA_HOME/lib/security/cacerts``
* Copy this file to a private location, for instance $HOME/pki/cacerts, and make it writable
* Using the same keytool command as the first solution above, add your custom certificates to this private truststore
  (the default password is again ``changeit``)
* In order to have DSS use it for all Java processes, you need to add command-line option
  ``-Djavax.net.ssl.trustStore=/PATH/TO/PRIVATE/TRUSTSTORE`` to all Java processes, using the procedure documented at
  :ref:`java.additional.options`

  .. code-block:: python

    [javaopts]
    backend.additional.opts = -Djavax.net.ssl.trustStore=/PATH/TO/PRIVATE/TRUSTSTORE
    jek.additional.opts = -Djavax.net.ssl.trustStore=/PATH/TO/PRIVATE/TRUSTSTORE
    fek.additional.opts = -Djavax.net.ssl.trustStore=/PATH/TO/PRIVATE/TRUSTSTORE
    hproxy.additional.opts = -Djavax.net.ssl.trustStore=/PATH/TO/PRIVATE/TRUSTSTORE

* Run ``dssadmin regenerate-config`` and restart DSS to complete the operation
