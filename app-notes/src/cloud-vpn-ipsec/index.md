# Dataiku Cloud VPN IPSEC

You can connect to your on-premise data sources using a site-to-site VPN leveraging the IPsec protocol.

Important:

* VPN IPsec is not available in all Dataiku plans. You may need to reach out to your Dataiku Account Manager or Customer Success Manager.
* You must allow Dataiku Cloud Public IPs to reach your VPN Gateway device. These IP addresses depend on your Dataiku Cloud region and are listed in the Launchpad connection forms.
* The private subnets exposed by your OpenVPN server or VPN IPSEC Gateway should not overlap with the following CIDR ranges: ``10.0.0.0/16``, ``10.1.0.0/16``, ``172.20.0.0/16``, ``10.11.0.0/16`` and ``10.94.0.0/16``.
* To enable VPN tunneling, the Dataiku instances need to be restarted. This operation could take up to 15 minutes.


## Create your configuration file

Dataiku Cloud relies on a StrongSwan-based VPN gateway using the ipsec.conf format. Here is a basic template file you can use for configuring the VPN IPSEC integration.

StrongSwan supports two types of configuration files: ipsec.conf and swanctl.conf. The Dataiku VPN integration uses the ipsec.conf file.

```
config setup
    # Line to increase vpn log level. Only uncomment if you need to debug the VPN connection
    # VPN logs are not available from the launchpad.
    # charondebug="ike 3, knl 3, cfg 3"
    uniqueids=no

conn ikev2-vpn-design
    type=tunnel
    keyexchange=ikev2
    authby=secret
    # The connection must be initiated by Dataiku since the VPN gateway is behind a NAT GW
    auto=start
    # The left side is the Dataiku side in this configuration
    left=%any
    # Left id is ofteh the Dataiku NAT GW IP address.
    leftid=<dataikunode-change-this-value>
    leftsubnet=10.0.0.0/16,10.1.0.0/16
    
    right=<your-vpn-gw-ip-address>
    rightid=<your-vpn-gw-ip-address>
    rightsubnet=<your-subnet-cidr-1>,<your-subnet-cidr-2> # example: 10.200.10.0/24,10.200.20.0/24
    
    # Optionally, specify the encryption algorithms you would like to use.
    # These are optional and automatically negotiated by the VPN Gateways by default.
    # ike=aes256gcm128-sha512-ecp384
    # esp=aes256gcm128-sha512-ecp384
```

## Create your secrets file

Currently, only secret key authentication is supported for IPSec. The ``secrets.conf`` file should appear as below:

```bash
# ipsec.secrets =this file holds shared secrets for authentication.
: PSK "your_secret_key"
```

## Add the extension on your Launchpad

Once you have created the required configuration and secrets files, you can actually create the extension on your Launchpad. If you need to create tunnels for both Design and Automation nodes, you will have to create separate configs.

To configure the VPN:

1. Go to Launchpad's **Extensions** panel.
2. Add the **IPsec** extension.
3. Input your created configuration and secrets files for all required nodes.
4. If needed, you can enable the source address translation. This will allow you to select the specific IP used by your Dataiku Cloud instances traffic.
5. Set the internal IP of your database as the host parameter for the connections that use the VPN tunnel.

* The translated address should be in the format ``A.B.C.D/M=X.Y.Z.T``, where ``A.B.C.D/M`` is the target subnet and ``X.Y.Z.T`` is the NAT gateway address.
* For example, if your target subnet is ``192.168.20.0/24`` and you expect traffic to come from ``192.168.10.1``, the translated address should be ``192.168.20.0/24=192.168.10.1``.

## Custom DNS

It is possible to use a custom DNS server. This setup works for both OpenVPN and VPN IPSec and is described in the Knowledge Base.
