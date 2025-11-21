# Compliance of DSS CloudStacks image with CIS Benchmark Server Level 1

The DSS CloudStacks virtual machine image is compliant with the CIS Benchmark - Server Level 1, version 2.2.0, with the following exceptions, for which we document the underlying reasoning.

## 1.3.2: Ensure filesystem integrity is regularly checked

DSS is compliant with this rule. Some CIS Benchmark checkers may report this incorrectly.

## 1.4.2: Ensure bootloader password is set

This control is not valid / relevant on the cloud and could interfere with boot

## 2.2.2: Ensure X Window System is not installed

The R programming environment depends on components of the X Window System. It should be noted that while the X Window System packages are installed, the X server is not running, and hence does not create an attack surface

## 3.4.3: Ensure /etc/hosts.deny is configured

Controlling network access to the DSS instance is done through cloud firewall rules / security groups instead

## 3.6.2: Ensure default deny firewall policy

Controlling network access to the DSS instance is done through cloud firewall rules / security groups instead

## 3.6.3: Ensure loopback traffic is configured

Controlling network access to the DSS instance is done through cloud firewall rules / security groups instead

## 3.6.5: Ensure firewall rules exist for all open ports

Controlling network access to the DSS instance is done through cloud firewall rules / security groups instead

## 4.2.14: Ensure rsyslog is configured to send logs to a remote log host

This is not part of the DSS setup, but can be configured by the administrator as a setup action

## 5.3.2: Ensure lockout for failed password attempts is configured

DSS is compliant with this rule. Some CIS Benchmark checkers may report this incorrectly. It should be noted that no user account across the machine has any password, so this rule is essentially irrelevant.

### 5.4.1.4: Ensure inactive password lock is 30 days or less

DSS is compliant with this rule. Some CIS Benchmark checkers may report this incorrectly. It should be noted that no user account across the machine has any password, so this rule is essentially irrelevant.

## 5.4.2: Ensure system accounts are non-login

The "dataiku" and "dkuadmin" user accounts are login by design, since DSS administrators may need to intervene on them. They have sub-1000 user identifiers because they are not "user accounts" per se.

All other system accounts are non-login

## 5.4.4: Ensure default user umask is 027 or more restrictive

Such a setting could interfere with DSS multi-user user isolation functioning

## 6.2.8: Ensure users home directories permissions are 750 or more restrictive

DSS User Isolation mechanism requires "traversal-only" access for "other" on the "dataiku" home directory. Notably, this does not provide a "read" access to the home.