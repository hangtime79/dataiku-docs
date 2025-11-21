The runtime databases
######################

.. contents::
    :local:

.. note::

    If using :doc:`Dataiku Cloud Stacks </installation/index>` installation, the runtime databases are automatically managed for you, and you do not need to follow these instructions.

    These instructions do not apply to Dataiku Cloud

DSS stores most of its configuration (including projects, datasets definition, code, notebooks, ...) as JSON, Python, R, ... files inside the ``config/`` folder of :doc:`the DSS data directory <datadir>`.

In addition, DSS maintains a number of databases, called the "runtime databases" that store some additional information, which is mostly "non-primary" information (i.e. which can be rebuilt):

* The history of run jobs and scenarios
* The history and latest values of metrics and checks
* The "state" of the datasets for the Flow's incremental computation
* The "human-readable" timelines of things that happened in projects
* The list of starred and watched objects
* The contents of discussions
* The user-entered metadata on external tables (in the data catalog)

By default, the runtime databases are hosted internally by DSS, using an embedded database engine (called H2). You can also move the runtime databases to an external PostgreSQL server. Moving the runtime databases to an external PostgreSQL server improves resilience, scalability and backup capabilities.

Managing internally-hosted runtime databases
==============================================

When the runtime databases are hosted internally by DSS, no maintenance is generally required.

Handling database failures
---------------------------

Please refer to the :doc:`dedicated error page </troubleshooting/errors/ERR_MISC_EIDB>`

Cleanup
-------

.. warning::

    Do not attempt to use the "Clean Internal Databases" macro when using runtime databases that are hosted internally by DSS

.. _runtime_db.external:

Externally hosting runtime databases
=====================================

Why use external hosting?
----------------------------

Externally hosting runtime databases has several advantages, especially for bigger production DSS instances:

* The internal H2 engine doesn't scale and perform as well as an external PostgreSQL server
* The external PostgreSQL server is more resilient to various failures than the internal H2 engine
* It's easier to back up a PostgreSQL server without any downtime

When to switch
---------------

* Generally speaking, it's preferable to use externally-hosted runtime databases
* All Dataiku Cloud Stacks setups already use externally-hosted runtime databases
* If possible, use externally-hosted runtime databases from the start
* You should switch usually at the direction of Dataiku Support or a Dataiku Field Engineer. Typically, when databases in the "databases/" folder exceed 1-2 GB.

Prerequisites and warnings
----------------------------

You need to have a PostgreSQL >= 9.5 server, with write access on a schema (including ability to create tables). There are no known issues with more recent PostgreSQL versions.

You can host the databases for multiple DSS instances in a single PostgreSQL server, including in a single schema, but you need
to make sure to set up a table prefix (see below).

.. warning::

    * You need to make sure that your PostgreSQL server will stay up. Downtime of the PostgreSQL server will completely prevent DSS operation, and may leave some jobs or scenarios in a broken state until DSS is restarted.

    * If you restart the PostgreSQL server, you **must** immediately restart DSS too.

PostgreSQL setup prerequisites and recommendations
----------------------------------------------------

We strongly recommend hosting the PostgreSQL server on the same machine as the DSS server. The databases require very low resources and can live alongside DSS without issue. Having both on the same machine ensure that they "restart together" (see the above warning) and also simplifies consistent backup (see the Backups section).

We advise against using cloud-managed databases such as AWS RDS, as they tend to go down from time to time (see the above warning).

We advise against using proxies such as PGBouncer.

You should configure the ``max_connections`` setting of your PostgreSQL server to at least 500. High ``max_connections`` have very low cost on PostgreSQL and there is no significant drawback to high ``max_connections``. Too low ``max_connections`` can fully prevent DSS from working. There is no direct correlation between "instance size", "what jobs do" and required connection count. 500 is sufficient for almost all instances.

Setup
------

* Stop DSS
* Edit ``config/general-settings.json`` and locate the ``"internalDatabase"`` key at top-level

* Fill it out as follows:

.. code-block:: javascript

        "internalDatabase": {
            "connection": {
                "params": {
                    "port": 15432,
                    "host": "HOST_OF_YOUR_POSTGRESQL_DATABASE",
                    "user": "USER_OF_YOUR_POSTGRESQL_DATABASE",
                    "password": "PASSWORD_OF_YOUR_POSTGRESQL_DATABASE",
                    "db": "DB_OF_YOUR_POSTGRESQL_DATABASE"
                },
                "type": "PostgreSQL"
            },

            "tableNamePrefix" : "optional prefix to prepend to all table names. Don't put this key if you don't want to use this. Should be used if you plan to have multiple DSS pointing to this database/schema",
            "schema" : "Name of the PostgreSQL schema in which DSS will create its tables",

            "externalConnectionsMaxIdleTimeMS": 600000,
            "externalConnectionsValidationIntervalMS": 180000,
            "maxPooledExternalConnections": 50,
            "builtinConnectionsMaxIdleTimeMS": 1800000,
            "builtinConnectionsValidationIntervalMS": 600000,
            "maxPooledBuiltinConnectionsPerDatabase": 50
        }

* Save the file
* Run the following command to copy the current content of your runtime databases to the PostgreSQL server:

.. code-block:: bash

    ./bin/dssadmin copy-databases-to-external

* Start DSS

Your DSS is now using externally-hosted runtime databases.

Backups
--------

You need to make sure to properly backup your PostgreSQL database using the regular PostgreSQL backup procedures. Each time you make a DSS backup, you should also ensure that you have a matching PostgreSQL backup.

The DSS backup and the PostgreSQL backup don't need to be perfectly synchronous, small discrepancies in backup times will not cause significant harm in case of a restore.

Migrations
-----------

When upgrading DSS, DSS will automatically upgrade the schema of the externally-hosted databases. Make sure to backup the databases before starting the DSS upgrade procedure in order to be able to roll back the DSS upgrade.

Advanced settings
-------------------

The "connection" part of the "internalDatabase" in ``config/general-settings.json`` is similar to the structure of a PostgreSQL connection in ``config/connections.json``. You can thus use advanced capabilities like JDBC-URL-based connection, advanced properties.

We recommend that you setup a PostgreSQL connection using the DSS UI, and then copy the relevant connection block from ``config/connections.json`` to ``config/general-settings.json``.

We highly discourage changing any of the "externalConnections" / "maxPooled..." settings without guidance from Dataiku Support.

Using an encrypted password
----------------------------

In order to avoid writing a password in cleartext in the configuration file, encrypt it first using:

.. code-block:: bash

    ./bin/dssadmin encrypt-password YOUR-PASSWORD

Use the encrypted password string (starting with ``e:AES:``) in the "password" field.
