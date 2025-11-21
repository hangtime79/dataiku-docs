Add SSH keys
------------

This setup action enables to add SSH keys to `~/.ssh` folder that can be used to connect to other machines from the DSS one.

To generate your public key on Dataiku Cloud:

* go to your launchpad > extension tab > add an extension,
* select the SSH integration feature,
* enter the hostnames of the remote that this key is allowed to connect to,
* click to validate and generate the key.

Dataiku Cloud will then automatically generate the key and run a command to the origin to get (and verify) the SSH host key of this server. You can now copy the generated key and add it to your hosts. To find this key in the future or generate a new one go to the extension tab and edit the SSH Integration feature.