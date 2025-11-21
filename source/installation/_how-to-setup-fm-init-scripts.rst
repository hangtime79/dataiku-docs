Howto: Install a script on your Fleet Manager to be run at VM restart time
##########################################################################

This application note documents how it is possible to install scripts on the Fleet Manager (FM) VM so that they are run when the VM is restarted.

Overview
***********

The FM startup process looks for folders ``/data/etc/dataiku-fm-init-scripts/{before|after}-startup.d`` in the VM. The shell executable scripts found in these folders will be executed in lexicographic order respectively before or after FM startup.

The logs for the different executions will be stored in ``/data/var/log/dataiku-fm-init-scripts/{before|after}-startup.d`` with the execution time in the file name.

Both scripts and script logs are available in FM diag.

Installing scripts
*********************

Let's take the example of a script to be executed before FM startup.

In order to install the script, SSH on the FM machine and run the following::

    sudo su root
    mkdir -p /data/etc/dataiku-fm-init-scripts/before-startup.d
    chown dataiku:dataiku /data/etc/dataiku-fm-init-scripts/before-startup.d
    cd /data/etc/dataiku-fm-init-scripts/before-startup.d
    touch test.sh
    chmod +x test.sh
    # implement your script in test.sh
    # change script folder to after-startup.d if you want the script to run after FM startup

Script examples
******************

Deprovision DSS nodes for the night
===================================

Overview
--------

This script will create all the necessary to install a system.d timer running every night at 8:00 PM in order to deprovision all the DSS machines listed in this FM instance.

Machine deprovisioning can be prevented by adding tag ``no-auto-deprovision`` to the machines needing it.

Script
------

Create an executable bash script in ``/data/etc/dataiku-fm-init-scripts/after-startup.d`` with the following code::

    #!/usr/bin/env bash

    # Get an API key and API secret for FM Python API
    output="$(sudo -u dataiku /data/dataiku/fmhome/bin/fmadmin create-personal-api-key admin /data/etc/dataiku-fm-init-scripts/after-startup.d/deprovision_fm_nodes_credentials.json)"

    # create the Python script deprovisioning the instances
    if [ ! -f /data/etc/dataiku-fm-init-scripts/after-startup.d/deprovision_fm_nodes.py ]; then
    cat > /data/etc/dataiku-fm-init-scripts/after-startup.d/deprovision_fm_nodes.py << EOF
    import dataikuapi
    import sys
    import json
    from pathlib import Path
    from dataikuapi.fm.instancesettingstemplates import FMSetupAction, FMSetupActionType

    FM_URL = "http://localhost:10000"
    NO_DEPROVISION_TAG = "no-auto-deprovision"

    def read_credentials(credentials_file_location):
        credentials_file_path = Path(credentials_file_location)
        if not credentials_file_path.is_file():
            raise Error("The provided credentials path does not match an existing JSON file")

        try:
            with open(credentials_file_location) as credentials_file:
                credentials_json = json.load(credentials_file)
            if not "id" in credentials_json or not "secret" in credentials_json:
                raise Error("The provided credentials file has incorrect JSON format")
        except:
            raise Error("The provided credentials file has incorrect JSON format")

        api_key = credentials_json["id"]
        api_secret = credentials_json["secret"]

        return api_key, api_secret

    def read_cloud():
        user_data_file_location = "/data/dataiku/fmhome/config/user-data.json"
        with open(user_data_file_location) as user_data_file:
            user_data = json.load(user_data_file)
        return str.lower(user_data['cloud'])

    def deprovision_instances(cloud, credentials_file_location):
        # Read credentials from the JSON file
        api_key, api_secret = read_credentials(credentials_file_location)

        # Create an FM client
        if cloud == "aws":
            print("Creating FM client for AWS")
            fm_client = dataikuapi.FMClientAWS(FM_URL, api_key, api_secret)
        elif cloud == "gcp":
            print("Creating FM client for GCP")
            fm_client = dataikuapi.FMClientGCP(FM_URL, api_key, api_secret)
        elif cloud == "azure":
            print("Creating FM client for Azure")
            fm_client = dataikuapi.FMClientAzure(FM_URL, api_key, api_secret)
        else:
            print(f"Unknown cloud provider: {cloud}")

        # List and display instances with their status in a table
        instances = fm_client.list_instances()
        futures = []

        print("Listing instances to be deprovisioned...")
        for instance in instances:
            if NO_DEPROVISION_TAG in instance.instance_data["fmTags"]:
                print(f"  - Skipping deprovision for instance with ID [{instance.instance_data['id']}]")
                continue
            instance_status = instance.get_status()
            if 'hasPhysicalInstance' in instance_status and instance_status['hasPhysicalInstance']:
                print(f"  - Scheduling deprovision for instance with ID [{instance.instance_data['id']}]")
                futures.append(instance.deprovision())

        print("Deprovisioning instances...")
        for future in futures:
            future.wait_for_result()

        print("Completed")

    if __name__ == "__main__":
        credentials_file_location = sys.argv[1]

        deprovision_instances(read_cloud(), credentials_file_location)
    EOF
    fi

    # Create system.d service file
    if [ -f /etc/systemd/system/deprovision_fm_nodes.timer ]; then
    systemctl stop deprovision_fm_nodes.timer
    rm -f /etc/systemd/system/deprovision_fm_nodes.timer
    fi

    if [ -f /etc/systemd/system/deprovision_fm_nodes.service ]; then
    rm -f /etc/systemd/system/deprovision_fm_nodes.service
    fi

    cat > /etc/systemd/system/deprovision_fm_nodes.service << EOF
    [Unit]
    Description="Deprovision DSS machines for the night"

    [Service]
    ExecStart=/data/dataiku/fmhome/pyenv/bin/python /data/etc/dataiku-fm-init-scripts/after-startup.d/deprovision_fm_nodes.py "/data/etc/dataiku-fm-init-scripts/after-startup.d/deprovision_fm_nodes_credentials.json"
    EOF

    # Create system.d corresponding timer file
    cat > /etc/systemd/system/deprovision_fm_nodes.timer << EOF
    [Unit]
    Description="Deprovision DSS nodes attached to this FM for the night"

    [Timer]
    OnCalendar=Mon..Fri *-*-* 20:00
    Unit=deprovision_fm_nodes.service

    [Install]
    WantedBy=multi-user.target
    EOF

    # Load the new files
    systemctl daemon-reload

    # Start timer
    systemctl start deprovision_fm_nodes.timer

    # Check timer status to have it in logs
    systemctl status deprovision_fm_nodes.timer

Provision DSS nodes in the morning
==================================

Overview
--------

This script will create all the necessary to install a system.d timer running every morning at 8:00 AM in order to provision all the DSS machines listed in this FM instance.

Machine provisioning can be prevented by adding tag ``no-auto-provision`` to the machines needing it.

Script
------

Create an executable bash script in ``/data/etc/dataiku-fm-init-scripts/after-startup.d`` with the following code::

    #!/usr/bin/env bash

    # Get an API key and API secret for FM Python API
    output="$(sudo -u dataiku /data/dataiku/fmhome/bin/fmadmin create-personal-api-key admin /data/etc/dataiku-fm-init-scripts/after-startup.d/provision_fm_nodes_credentials.json)"

    # create the Python script provisioning the instances
    if [ ! -f /data/etc/dataiku-fm-init-scripts/after-startup.d/provision_fm_nodes.py ]; then
    cat > /data/etc/dataiku-fm-init-scripts/after-startup.d/provision_fm_nodes.py << EOF
    import dataikuapi
    import sys
    import json
    from pathlib import Path
    from dataikuapi.fm.instancesettingstemplates import FMSetupAction, FMSetupActionType

    FM_URL = "http://localhost:10000"
    NO_PROVISION_TAG = "no-auto-provision"

    def read_credentials(credentials_file_location):
        credentials_file_path = Path(credentials_file_location)
        if not credentials_file_path.is_file():
            raise Error("The provided credentials path does not match an existing JSON file")

        try:
            with open(credentials_file_location) as credentials_file:
                credentials_json = json.load(credentials_file)
            if not "id" in credentials_json or not "secret" in credentials_json:
                raise Error("The provided credentials file has incorrect JSON format")
        except:
            raise Error("The provided credentials file has incorrect JSON format")

        api_key = credentials_json["id"]
        api_secret = credentials_json["secret"]

        return api_key, api_secret

    def read_cloud():
        user_data_file_location = "/data/dataiku/fmhome/config/user-data.json"
        with open(user_data_file_location) as user_data_file:
            user_data = json.load(user_data_file)
        return str.lower(user_data['cloud'])

    def provision_instances(cloud, credentials_file_location):
        # Read credentials from the JSON file
        api_key, api_secret = read_credentials(credentials_file_location)

        # Create an FM client
        if cloud == "aws":
            print("Creating FM client for AWS")
            fm_client = dataikuapi.FMClientAWS(FM_URL, api_key, api_secret)
        elif cloud == "gcp":
            print("Creating FM client for GCP")
            fm_client = dataikuapi.FMClientGCP(FM_URL, api_key, api_secret)
        elif cloud == "azure":
            print("Creating FM client for Azure")
            fm_client = dataikuapi.FMClientAzure(FM_URL, api_key, api_secret)
        else:
            print(f"Unknown cloud provider: {cloud}")

        # List and display instances with their status in a table
        instances = fm_client.list_instances()
        futures = []

        print("Listing instances to be provisioned...")
        for instance in instances:
            if NO_PROVISION_TAG in instance.instance_data["fmTags"]:
                print(f"  - Skipping provision for instance with ID [{instance.instance_data['id']}]")
                continue
            instance_status = instance.get_status()
            if 'hasPhysicalInstance' in instance_status and not instance_status['hasPhysicalInstance']:
                print(f"  - Scheduling provision for instance with ID [{instance.instance_data['id']}]")
                futures.append(instance.reprovision())

        print("Provisioning instances...")
        for future in futures:
            future.wait_for_result()

        print("Completed")

    if __name__ == "__main__":
        credentials_file_location = sys.argv[1]

        provision_instances(read_cloud(), credentials_file_location)
    EOF
    fi

    # Create system.d service file
    if [ -f /etc/systemd/system/provision_fm_nodes.timer ]; then
    systemctl stop provision_fm_nodes.timer
    rm -f /etc/systemd/system/provision_fm_nodes.timer
    fi

    if [ -f /etc/systemd/system/provision_fm_nodes.service ]; then
    rm -f /etc/systemd/system/provision_fm_nodes.service
    fi

    cat > /etc/systemd/system/provision_fm_nodes.service << EOF
    [Unit]
    Description="Provision DSS machines in the morning"

    [Service]
    ExecStart=/data/dataiku/fmhome/pyenv/bin/python /data/etc/dataiku-fm-init-scripts/after-startup.d/provision_fm_nodes.py "/data/etc/dataiku-fm-init-scripts/after-startup.d/provision_fm_nodes_credentials.json"
    EOF

    # Create system.d corresponding timer file
    cat > /etc/systemd/system/provision_fm_nodes.timer << EOF
    [Unit]
    Description="Provision DSS nodes attached to this FM in the morning"

    [Timer]
    OnCalendar=Mon..Fri *-*-* 08:00
    Unit=provision_fm_nodes.service

    [Install]
    WantedBy=multi-user.target
    EOF

    # Load the new files
    systemctl daemon-reload

    # Start timer
    systemctl start provision_fm_nodes.timer

    # Check timer status to have it in logs
    systemctl status provision_fm_nodes.timer
