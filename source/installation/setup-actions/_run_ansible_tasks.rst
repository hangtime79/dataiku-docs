Run Ansible tasks
-----------------

This setup action allows you to run arbitrary ansible tasks at different point of the startup process.

The **Stage** parameter specificies at which point of the startup sequence it must be executed. There is three stages:

- **Before DSS install**: These tasks will be run before the agent installs (if not already installed) or upgrades (if required) DSS.
- **After DSS install**: These tasks will be run once DSS is installed or upgraded, but not yet started.
- **After DSS is started**: These tasks will be run once DSS is ready to receive public API calls from the agent.


The **Ansible tasks** allows you to Write a YAML list of ansible tasks as if they were written in a role. Available tasks are base Ansible
tasks and `Ansible modules for Dataiku DSS <https://github.com/dataiku/dataiku-ansible-modules>`_. When using Dataiku modules, it is not
required to use the connection and authentication options. It is automatically handled by FM.

Some additional facts are available:

- `dataiku.dss.port`
- `dataiku.dss.datadir`
- `dataiku.dss.version`
- `dataiku.dss.node_id`: Identifier matching the node id in Fleet Manager, unique per fleet
- `dataiku.dss.node_type`: Node type is either `design`, `automation`, `deployer` or `govern` 
- `dataiku.dss.logical_instance_id`: Unique ID that identifies this instance in the Fleet Manager
- `dataiku.dss.instance_type`: The cloud instance type (also referred to as instance size) used to run this instance
- `dataiku.dss.was_installed`: Available only for stages **After DSS install** and **After DSS startup**
- `dataiku.dss.was_upgraded`: Available only for stages **After DSS install** and **After DSS startup**
- `dataiku.dss.api_key`: Available only for stage **After DSS startup**

Example:

.. code-block:: YAML

  ---
  - dss_group:
      name: datascienceguys
  - dss_user:
      login: dsadmin
      password: verylongbutinsecurepassword
      groups: [datascienceguys]


Ansible is ran with the unix user held by the agent, and can run administrative tasks with `become`.
