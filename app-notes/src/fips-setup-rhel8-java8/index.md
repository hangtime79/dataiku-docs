# Installing DSS on RHEL 8 with FIPS mode enabled

Starting with version 11.4, DSS can be installed on selected environments compatible with the Federal Information Processing Standard (FIPS) 140-2.

This note describes such a setup, based on Red Hat Enterprise Linux 8, Java 8, and the BouncyCastle FIPS-compliant security providers for Java.

Note that running the BouncyCastle providers in "FIPS approved mode" is not supported under this setup.

## 1. Operating system installation

Starting from a RHEL base system version 8.3 or later, enable FIPS mode following [Red Hat documentation](https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/8/html/security_hardening/assembly_installing-a-rhel-8-system-with-fips-mode-enabled_security-hardening).

Typically, you would need to run the following commands as root:
```
# fips-mode-setup --enable
# reboot
```

Install the latest version of the RedHat-provided OpenJDK 1.8 package:
```
# dnf install java-1.8.0-openjdk-devel
```

## 2. Install the BouncyCastle FIPS-compliant cryptography libraries in the JDK

Connect to `https://www.bouncycastle.org/fips-java/` and download the latest versions of the base (`bc-fips`), PKIX (`bcpkix-fips`) and TLS (`bctls-fips`) cryptography providers. At the time of writing, these are:
```
bc-fips-1.0.2.3.jar
bcpkix-fips-1.0.7.jar
bctls-fips-1.0.15.jar
```

Newer versions of these libraries should work but have not been tested by Dataiku.

Install these three files in the extension library directory of the target Java runtime, ie `JAVA_HOME/jre/lib/ext`. If this Java runtime is the default one on the server, that would be: `/usr/lib/jvm/java-1.8.0-openjdk/jre/lib/ext`

These files should be installed with owner root, group root and permission mode 0644.


## 3. Configure the JDK to use the BouncyCastle cryptography providers

Edit the security configuration file of the target Java runtime, located at `JAVA_HOME/jre/lib/security/java.security` (as root):

- Locate the block of lines configuring the FIPS-mode security providers (`fips.provider.N`) and replace it with:
```
fips.provider.1=org.bouncycastle.jcajce.provider.BouncyCastleFipsProvider
fips.provider.2=org.bouncycastle.jsse.provider.BouncyCastleJsseProvider fips:BCFIPS
fips.provider.3=sun.security.provider.Sun
fips.provider.4=sun.security.ec.SunEC
fips.provider.5=com.sun.net.ssl.internal.ssl.Provider BCFIPS
```

- Locate the definitions for `fips.keystore.type` and `ssl.KeyManagerFactory.algorithm`, and replace them with:
```
fips.keystore.type=PKCS12
ssl.KeyManagerFactory.algorithm=PKIX
```

## 4. DSS installation

You can now install and run DSS following the standard procedure, making sure it uses the Java runtime which you have configured above.

If this Java runtime is not the default one on the server, you would need to define the `JAVA_HOME` environment variable accordingly, as in:
```
export JAVA_HOME=/usr/lib/jvm/java-1.8.0-openjdk
```
