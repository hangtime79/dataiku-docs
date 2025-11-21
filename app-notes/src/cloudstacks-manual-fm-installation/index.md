---
title: "Cloud Stacks: Manual Fleet Manager setup and operation"
---

This section deals with manually setting up Fleet Manager (rather than using a Cloud Formation, Azure Resource Manager, or GCP template


We **strongly** recommend using our Cloud Formation or similar based setup. This documentation is only to be used for advanced and specific use cases. Manually installing and managing Fleet Manager loses some of the fully-managed advantages of using Cloud Stacks.


# Manually installing FM

## Requirements

### Cloud instance

FM must be installed on a Linux cloud instance instance.

A minimum of 4 GB of RAM is required. No CPU minimum is required.

The following Linux distributions are supported:

* Red Hat Enterprise Linux, versions 8.x
* AlmaLinux, versions 8.4 and later 8.x

These distributions should be up-to-date with respect to Linux patches and updates.

### Other system requirements

The en_US.utf8 locale must be installed.

The filesystem on which FM is installed must be POSIX compliant, case-sensitive, support POSIX file locks and symbolic links.

### Unix user

FM runs as a single Unix user. FM does not run as root. We recommend dedicating a UNIX user for FM. In the rest of this documentation, this will be refered to as ``the fmuser``.

Root access is not strictly required, but you might need it to install dependencies. If you want to start FM at machine boot time, root access is required.

### Network requirements (AWS)


The EC2 instance on which FM is installed must be running in EC2-VPC. FM must be able to reach EC2, KMS, STS and SecretsManager endpoints. This can be achieved either by allowing traffic to public endpoints (through Internet Gateway, Egress Gateway or NAT Gateway), or with private endpoints deployed in your VPC.

FM may use up to 10 consecutive TCP ports. Only the first of these ports needs to be opened out of the machine. It is highly recommended to firewall the other ports.

You must be able to connect to the base port with your browser. You can allow direct connection or use a reverse-proxy. 

### Network requirements (Azure)


The VM instance on which FM is installed must be running in EC2-VPC. FM must be able to reach the Azure management endpoints

FM may use up to 10 consecutive TCP ports. Only the first of these ports needs to be opened out of the machine. It is highly recommended to firewall the other ports.

You must be able to connect to the base port with your browser. You can allow direct connection or use a reverse-proxy. 


### KMS CMK (AWS)

You must create a KMS CMK. The IAM role of FM must have the ability to use this CMK.

### IAM permissions (AWS)

The EC2 instance on which FM is installed must have IAM credentials available to the fmuser.

This can be achieved either:

* Through an IAM instance profile associated to the instance (recommended)
* Through a keypair available in the ``~/.aws/credentials`` of the fmuser

The required IAM permissions are:

* Full control on EC2
* Manage secrets using the previously created CMK

Additional recommended permissions:

* Full control of a Route53 zone to host records for private IPs
* Full control of a Route53 zone to host records for public IPs


### Browser

The following browsers are supported:

* Chrome (latest version)
* Firefox (latest ESR version)

### Database

FM requires a PostgreSQL 10 (or higher) database for storing data. We strongly recommend using a locally-installed PostgreSQL.

PostgreSQL managed by your cloud, such as RDS or Aurora is also usable.


### Installation folders

A FM installation spans over two folders:

* The installation directory, which contains the code of FM. This is the directory where the FM tarball is unzipped (denoted as "INSTALL_DIR")
* The data directory (denoted as "DATA_DIR").

The data directory contains :

* The configuration of FM
* Log files for the server components
* Startup and shutdown scripts and command-line tools


### Preparing install

To install FM, you need the installation tarball and a license file obtained from Dataiku.

## Installation

Unpack the tar.gz in the location you have chosen for the installation directory.


	cd SOMEDIR
	tar xfp /PATH/TO/dataiku-fm-VERSION.tar.gz
	# This creates a directory named dataiku-fm-VERSION in the current directory
	# which contains FM code for this version (no user file is written to it by FM).
	# This directory is referred to as INSTALL_DIR in this document.


From the fmuser account, run

	dataiku-fm-VERSION/installer.sh -c AWS -d /path/to/DATA_DIR -p PORT -l LICENSE_FILE
	# Replace AWS by Azure or GCP as needed


Where:

* DATA_DIR is the location of the data directory that you want to use. If the directory already exists, it must be empty.
* PORT is the base TCP port.
* LICENSE_FILE is your FM license file.


DATA_DIR must be outside of the install dir (i.e. DATA_DIR must not be within dataiku-fm-VERSION)


The installer automatically checks for any missing system dependencies. If any is missing, it will give you the command to run to install them with superuser privileges. After installation of dependencies is complete, you can start the FM installer again, using the same command as above.

### Enable startup at boot time

At the end of installation, FM will give you the optional command to run with superuser privileges to configure automatic boot-time startup:


	sudo -i INSTALL_DIR/scripts/install/install-boot.sh DATA_DIR USER_ACCOUNT


## Setup FM settings

Edit the ```DATA_DIR/config/settings.json``` file.

* Edit the value ``databaseSettings.dbURL`` to setup the connection to the database.

* Setup the "awsSettings", "azureSettings" or "gcpSettings" in the same file.

* Set "tenancy" to "MONOTENANT"

Save the file

## Bootstrap the database

Now that FM can connect to the database, run the following command to initialize the data in the database:


	DATA_DIR/bin/fmadmin initial-setup USER PASSWORD

where:

* USER is the new login of the admin user for FM
* PASSWORD is the new password of the admin user for FM

## Start

To start FM, run the following command:


	DATA_DIR/bin/fm start

## Configure the CMK into FM (AWS)

Connect to FM with your initial user. In the *Cloud setup* section, click on *Edit*, fill the *CMK Id* field and click on *Save*.


FM is ready, you can proceed to the setup of virtual networks. Follow the usual Cloud Stacks documentation



# Manually upgrading FM

In the rest of this procedure, DATA_DIR denotes the location of the FM Data directory.

## Notes and limitations

For each version of FM, we publish release notes as part of the regular DSS release notes which indicate the detailed limitations, attention points and notes about release. We strongly advise that you read all release notes for the new FM version before starting the upgrade.

NOTE that given that this is an exotic/non-standard setup, release notes for DSS may not include required instructions for manual FM upgrades

## Pre-upgrade tasks

Before upgrading, it is very highly recommended to backup the whole content of the data directory.

## Upgrade

Stop the old version

    DATA_DIR/bin/fm stop

Unpack the distribution tarball in the location you have chosen for the new installation directory.


    cd SOMEDIR
    tar xzf /PATH/TO/dataiku-fm-NEWVERSION.tar.gz
    # This creates installation directory SOMEDIR/dataiku-fm-NEWVERSION for the new version

Perform the upgrade:


    dataiku-fm-NEWVERSION/installer.sh -d DATA_DIR -u

Like for normal install, FM will check for missing system dependencies, and ask you to run a dependencies installation command with superuser privileges if needed.

FM may ask you to confirm migration of the existing data directory

Start the new version:


    DATA_DIR/bin/fm start


# Advanced FM Setup


## HTTPS and reverse proxies

There are several configurations where you may want to do:

* If you want to expose FM to your users on a different host and/or port than its native installation, you need
  to configure a reverse proxy in front of FM. This is the case in particular if you want to expose FM on the
  standard HTTP/80 or HTTPS/443 ports, as FM should not run with superuser privileges.

## Configuring a reverse proxy in front of FM

The following configuration snippets can be adapted to forward FM interface through an external nginx or Apache web server,
to accomodate deployments where users should access it through a different base URL than that of its native host and port installation
(for example to expose FM on the standard HTTP port 80, or on a different host name).


FM cannot be remmaped to a base URL with a non-empty path prefix (that is, to http://HOST:PORT/PREFIX/ where PREFIX is not empty).


### HTTP deployment behind a nginx reverse proxy

    # nginx reverse proxy configuration for Dataiku FM
    # requires nginx version 1.4 or above
    server {
        # Host/port on which to expose FM to users
        listen 80;
        server_name fm.example.com;
        location / {
            # Base url of the FM installation
            proxy_pass http://FM_HOST:FM_PORT/;
            proxy_redirect off;
            # Allow long queries
            proxy_read_timeout 3600;
            proxy_send_timeout 600;
            # Allow large uploads
            client_max_body_size 0;
            # Allow protocol upgrade to websocket
            proxy_http_version 1.1;
            proxy_set_header Host $http_host;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
        }
    }

### HTTPS deployment behind a nginx reverse proxy

FM can also be accessed using secure HTTPS connections, provided you have a valid certificate for the host name on which it should be visible
(some browsers do not accept secure WebSocket connections using untrusted certificates).

You can configure this by deploying a nginx reverse proxy server, on the same or another host than FM,
using a variant of the following configuration snippet:


    # nginx SSL reverse proxy configuration for Dataiku FM
    # requires nginx version 1.4 or above
    server {
        # Host/port on which to expose FM to users
        listen 443 ssl;
        server_name fm.example.com;
        ssl_certificate /etc/nginx/ssl/fm_server_cert.pem;
        ssl_certificate_key /etc/nginx/ssl/fm_server.key;
        location / {
            # Base url of the FM installation
            proxy_pass http://FM_HOST:FM_PORT/;
            proxy_redirect off;
            # Allow long queries
            proxy_read_timeout 3600;
            proxy_send_timeout 600;
            # Allow large uploads
            client_max_body_size 0;
            # Allow protocol upgrade to websocket
            proxy_http_version 1.1;
            proxy_set_header Host $http_host;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
        }
    }


Also set "secureCookies": true in settings.json


### HTTP deployment behind an Apache reverse proxy

The following configuration snippet can be used to forward FM through an Apache HTTP server:


    # Apache reverse proxy configuration for Dataiku FM
    # requires Apache version 2.4.5 or above
    LoadModule proxy_module modules/mod_proxy.so
    LoadModule proxy_http_module modules/mod_proxy_http.so
    LoadModule proxy_wstunnel_module modules/mod_proxy_wstunnel.so
    LoadModule rewrite_module modules/mod_rewrite.so

    <VirtualHost *:80>
        ServerName fm.example.com
        RewriteEngine On
        RewriteCond %{HTTP:Connection} Upgrade [NC]
        RewriteCond %{HTTP:Upgrade} WebSocket [NC]
        RewriteRule /(.*) ws://FM_HOST:FM_PORT/$1 [P]
        RewriteRule /(.*) http://FM_HOST:FM_PORT/$1 [P]
        ProxyPassReverse / http://FM_HOST:FM_PORT/
        ProxyPreserveHost on
        ProxyTimeout 3600
    </VirtualHost>



## Installation configuration file

The installation process for FM can be customized through the ``DATADIR/install.ini`` configuration file.

This file is initialized with default values when the data directory is first created. It can be edited to specify
a number of non-default installation options, which are then preserved upon upgrades.

Modifying this file requires running a post-installation command to propagate the changes, and restarting FM, as follows:

  
    # Stop FM
    DATADIR/bin/fm stop
    # Edit installation options
    vi DATADIR/install.ini
    # Regenerate FM configuration according to the new settings
    DATADIR/bin/fmadmin regenerate-config
    # Restart FM
    DATADIR/bin/fm start

The ``install.ini`` installation configuration file is a standard INI-style `Python configuration file
<https://docs.python.org/2/library/configparser.html>`_ with ``[section]`` headers followed by ``key = value`` entries.
The following entries are set up by the initial installation and are mandatory:

    [general]
    nodetype = fm
    [server]
    port = 10000

Additional installation options are described throughout this manual.


## Java configuration

FM is a Java application, and requires a compatible Java environment to run. Supported versions are `OpenJDK <http://openjdk.java.net>`_ and
`Oracle JDK <https://www.oracle.com/technetwork/java/javase/downloads/index.html>`_, versions 8, 10, or 11.

Unless instructed otherwise (see :ref:`below <java.custom_jre>`) the FM installer will automatically look for a suitable version of Java
in standard locations. If none is found, it will install an appropriate OpenJDK package as part of its dependency installation phase.

While the Java Runtime Environment (JRE) is technically sufficient for FM to run, it is strongly recommended to install the full Java Development Kit (JDK) as this includes additional tools for diagnosing performance and other technical issues.
  Dataiku support may require you to install the full JDK to investigate some cases.


You can force FM to use a specific version of Java (for example, when there are several versions installed on the
server, or when you manually installed Java in a non-standard place) by setting the **DKUJAVABIN** environment variable
while running the FM installer script. This variable should point to the java binary to use. For example:


    $ DKUJAVABIN=/usr/local/bin/java dataiku-fm-VERSION/installer.sh <INSTALLER_OPTIONS>

Note that the installer script stores this value in the file ``DATA_DIR/bin/env-default.sh``, so this environment variable is only needed
at installation time. It must be provided for all subsequent FM updates however, unless one wishes FM to revert to the automatically-detected
version of Java.


You can switch an existing FM instance to an different version of Java by rerunning the installer
in update mode with a new value for **DKUJAVABIN**, as follows:


    # Stop FM
    $ FM_DATADIR/bin/fm stop
      
    # Switch this FM instance to a different Java runtime
    $ DKUJAVABIN=/PATH/TO/NEW/java dataiku-fm-VERSION/installer.sh -d FM_DATADIR -u
     
    # Restart FM
    $ FM_DATADIR/bin/fm start


### Customizing Java runtime options

The FM installer generates a default set of runtime options for the FM Java processes, based on the Java version in use and the
memory size of the hosting server. These options can be customized if needed.

FM is made up of 1 single kind of Java process, the "fmmain" process is the main server

All Java options of this process can be customized.

For each of these, FM provides an easy way to:

* configure the amount of memory allocated to each process (Java "-Xmx")
* add custom options

These customizations can be done by editing the install.ini file

More advanced customization (taking precedence over default FM options) can be done via environment files.

#### Customizing maximum memory size (xmx)

Most often, you will want to customize the amount of memory ("xmx") variable, which is the maximum memory allocated to the Java process.

Xmx is configured by setting the ``<processtype>.xmx`` setting in the ``javaopts`` section of the install.ini file (where ``<processtype>`` is fmmain

The installer sets Xmx to a default value between 2 and 6 GB, depending on the memory size of the host. This might not be enough for FM instances
with a large number of users. If that amount of memory is not sufficient, the FM backend may crash, and all users would get disconnected until
it automatically restarts.

* Go to the FM data directory

* Stop FM

    ```
    ./bin/fm stop
    ```


* Edit the install.ini file

* If it does not exist, add a ``[javaopts]`` section

* Add a line: ``fmmain.xmx = 2g``

* Regenerate the runtime config:

    ```
    ./bin/fmadmin regenerate-config
    ```

* Start FM

    ```
    ./bin/fm start
    ```

#### Adding additional Java options

You can add arbitrary options to the FM Java processes. Use the same procedure as above, with ``<processtype>.additional.opts``
directives:


    [javaopts]
    fmmain.additional.opts = -Dmy.option=value


#### Advanced customization

The full Java runtime options can be configured by setting environment variables in the DATA_DIR/bin/env-site.sh file in the FM
data directory.

You should only use this section if you could not obtain the desired set of options using the options above.

The default runtime options are stored in several environment variables:

* DKU_FMMAIN_JAVA_OPTS

The default values for these files (computed from install.ini) are stored in the DATA_DIR/bin/env-default.sh.


Do not modify DATA_DIR/bin/env-default.sh, it would get overwritten at the next FM upgrade and after each call to ``./bin/fmadmin regenerate-config``

To configure these options:

* Stop FM


    ./bin/fm stop

* Open the bin/env-default.sh file
* Copy the line you want to change. They look like ``export DKU_BACKEND_JAVA_OPTS``, ``export DKU_JEK_JAVA_OPTS``, ...
* Open the DATA_DIR/bin/env-site.sh file
* Paste the line and modify it to your needs

* Start FM

    ./bin/fm start


### Adding SSL certificates to the Java truststore

There are a number of configurations where FM needs to connect to external resources using secure network connections (SSL / TLS). This
includes (but is not limited to):

* connecting to a secure LDAP server
* connecting to Hadoop components (Hive, Impala) over SSL-based connections
* connecting to SQL databases, MongoDB, Cassandra, ... over secure connections

In all these cases, the Java runtime used by FM needs to be able to verify the identity of the remote server, by checking that its certificate
is derived from a trusted certification authority. The JVM comes with a default list of well-known Internet-based certification authorities,
which normally covers all legitimate publicly-accessible Internet resources. However, resources internal to your organization are typically
certified by private certification authorities, or by standalone (self-signed) certificates. It is then necessary to add additional certificates
to the trusted list of the JVM used by FM (a.k.a. truststore).

You should refer to the documentation of your JVM and/or Linux distribution for the precise procedure for this. In most cases, you can use one of
the following options:

#### Add a local certificate to the global JVM truststore


You will need write access to the Java installation for this (that would be root access for the typical case where the JVM has been installed
through a package manager).

* check which JVM is used by FM by looking for variable ``DKUJAVABIN`` in file ``DATADIR/bin/env-default.sh``
* locate the physical installation directory of this JVM with : ``readlink -f /PATH/TO/java``. This should resolve to ``JAVA_HOME/jre/bin/java``  where JAVA_HOME is the installation directory for this JVM.
* locate the default truststore file, at ``JAVA_HOME/jre/lib/security/cacerts``
* prepare the certificate(s) to add, in one of the supported file formats (binary- or base64-encoded DER, typically named .pem, .cer, .crt,
  or .der, or PKCS#7 certificate chain, typically named .p7b, or .p7c)
* import your certificate in the JVM trustore with ``keytool`` (the certificate store management tool, shipped with the JVM).
  This command prompts for the trustore password, which by default is ``changeit`` on Oracle and OpenJDK distributions.


    keytool -import [-alias FRIENDLY_NAME] -keystore /PATH/TO/cacerts -file /PATH/TO/CERT_TO_IMPORT

  You may need to first make this file writable with chmod, if it is write-protected.

  You can check that the import was successful by listing the new truststore contents:


    keytool -list -keystore /PATH/TO/cacerts

You need to restart FM after this operation.


This operation may need to be redone after an update of the JVM, or of the global system-wide certificate trust list.


Instead of directly modifying the default trustore at ``JAVA_HOME/jre/lib/security/cacerts``, you can duplicate it to a file
  named ``jssecacerts`` in the same directory, and update this file instead. When this file exists, it overrides the default one,
  which lets you preserve the original, distribution-provided version.

For full reference to the management of SSL certificate trust stores, refer to the documentation of your Java runtime.
  
For Oracle JRE, you can refer to:

  * http://docs.oracle.com/javase/8/docs/technotes/guides/security/jsse/JSSERefGuide.html#CustomizingStores
  * http://docs.oracle.com/javase/8/docs/technotes/tools/unix/keytool.html



#### Add a local certificate to the system-wide certificate trust list

You need to be root for this operation.

Most Unix distributions maintain and distribute a system-wide trusted certificate list, which is in turn used by the various subsystems which need
it, including all distribution-installed JVMs. Following distributions-specific procedures to add custom certificates to this list ensures that
these additions are not lost upon system or JVM updates, and are available to other subsystems as well (eg command-line tools).

On RedHat / CentOS / AlmaLinux systems, the global trustore is built with ``update-ca-trust(8)`` as follows (refer to the manpage for details):

* (as root) add any local certificates to trust in directory ``/etc/pki/ca-trust/source/anchors/``
* (as root) run : ``update-ca-trust extract``
* optionally, check with: ``keytool -list -keystore JAVA_HOME/jre/lib/security/cacerts -storepass changeit``

On Debian / Ubuntu systems, the global truststore is built with ``update-ca-certificates(8)`` as follows (refer to the manpage for details):

* (as root) add any local certificates to trust in directory ``/usr/local/share/ca-certificates`` (or a subdirectory of it), as a file
  with extension ".crt"
* (as root) run : ``update-ca-certificates``
* optionally, check with: ``keytool -list -keystore JAVA_HOME/jre/lib/security/cacerts -storepass changeit``

You need to restart FM after this operation.


#### Run FM with a private truststore

If you lack administrative access required to update the global truststore (system-wide, or JVM default), you can copy the global trustore to a
private location, add your custom certificates to it, and direct FM to use it instead of the default trustore.

* Using the same steps as the first solution above, locate the default JVM truststore at ``JAVA_HOME/jre/lib/security/cacerts``
* Copy this file to a private location, for instance $HOME/pki/cacerts, and make it writable
* Using the same keytool command as the first solution above, add your custom certificates to this private truststore
  (the default password is again ``changeit``)
* In order to have FM use it for all Java processes, you need to add command-line option
  ``-Djavax.net.ssl.trustStore=/PATH/TO/PRIVATE/TRUSTSTORE`` to all Java processes, using the procedure documented at
  :ref:`java.additional.options`


    [javaopts]
    backend.additional.opts = -Djavax.net.ssl.trustStore=/PATH/TO/PRIVATE/TRUSTSTORE
    jek.additional.opts = -Djavax.net.ssl.trustStore=/PATH/TO/PRIVATE/TRUSTSTORE
    fek.additional.opts = -Djavax.net.ssl.trustStore=/PATH/TO/PRIVATE/TRUSTSTORE
    hproxy.additional.opts = -Djavax.net.ssl.trustStore=/PATH/TO/PRIVATE/TRUSTSTORE

* Run ``fmadmin regenerate-config`` and restart FM to complete the operation

## Configuring IPv6 support

By default, FM listens to IPv4 connections only. Using the following installation configuration directive, you can configure FM to listen to IPv6
connections to its base port, in addition to IPv4 connections.

  
    [server]
    ipv6 = true

You should then regenerate FM configuration and restart FM, as described in :ref:`install.ini`.


