# Installing DSS on RHEL 8 with FIPS mode enabled

Starting with version 11.4, DSS can be installed on selected environments compatible with the Federal Information Processing Standard (FIPS) 140-2.

This note describes such a setup, based on Red Hat Enterprise Linux 8, Java 11, and the BouncyCastle FIPS-compliant security providers for Java.

Note that running the BouncyCastle providers in "FIPS approved mode" is not supported under this setup.

## 1. Operating system installation

Starting from a RHEL base system version 8.3 or later, enable FIPS mode following [Red Hat documentation](https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/8/html/security_hardening/assembly_installing-a-rhel-8-system-with-fips-mode-enabled_security-hardening).

Typically, you would need to run the following commands as root:
```
# fips-mode-setup --enable
# reboot
```

Install the latest version of the RedHat-provided OpenJDK 11 package, including the Java modules (JMods):
```
# dnf install java-11-openjdk-devel java-11-openjdk-jmods
```

## 2. Customize the OpenSAML 4 Library for FIPS Compliance

OpenSAML 4 does not provide a FIPS-compliant version of their library out of the box. To create a FIPS-compliant version, follow these steps:

### Steps to Remove the NamedCurve Configuration:

At the time of writing, the OpenSAML version used by DSS is `4.3.1`.

1. **Locate the JAR file:**

   Navigate to the directory where `opensaml-security-api-4.3.1.jar` is stored, typically `lib/ivy/common-run/`.

2. **Extract the JAR file:**

   Use a tool like `unzip` to extract the contents of the JAR file.
   ```sh
   cd lib/ivy/common-run/
   unzip opensaml-security-api-4.3.1.jar -d opensaml-extracted
   ```

3. **Remove the NamedCurve Configuration:**

   Navigate to the `META-INF/services/` directory within the extracted files.
   ```sh
   rm opensaml-extracted/META-INF/services/org.opensaml.security.crypto.ec.NamedCurve
   ```

4. **Repack the JAR file:**

   Repack the JAR file without the `NamedCurve` configuration file.
   ```sh
   jar cf opensaml-security-api-4.3.1.jar -C opensaml-extracted .
   ```

6. **Clean up:**
   Remove the temporary extracted directory.
   ```sh
   rm -rf opensaml-extracted
   ```

## 3. Customize the Snowflake JDBC Library

Snowflake offers a FIPS-compliant version of their JDBC library. To use this version, follow these steps:

1.	**Identify the Current Snowflake JDBC Version:**

   Before downloading the FIPS-compliant version, you need to identify the current version used by DSS. Check the lib/ivy/jdbc-snowflake/ directory to find the existing JAR file.

   ```sh
   ls lib/ivy/jdbc-snowflake/
   ```

   Look for a file with a name like snowflake-jdbc-<version>.jar. Note down the version number.
   At the time of writing, the snowflake jdbc version used by DSS is `3.14.4`.

2. **Download the Snowflake JDBC FIPS-compliant JAR:**

   Download it from [here](https://mvnrepository.com/artifact/net.snowflake/snowflake-jdbc-fips/3.14.4).

3. **Place the JAR in the Appropriate Directory:**

   Move the downloaded JAR to the `lib/ivy/jdbc-snowflake/` directory.
   ```sh
   mv path/to/snowflake-jdbc-fips-3.14.4.jar lib/ivy/jdbc-snowflake/
   ```
4. **Remove the Pre-existing JAR:**

   Delete the non-FIPS-compliant JAR from the same directory.
   ```sh
   rm lib/ivy/jdbc-snowflake/snowflake-jdbc-3.14.4.jar
   ```

## 4. Replace the BouncyCastle cryptography libraries with their equivalent FIPS versions

Remove from the DSS kit, the following jars:

```sh
rm lib/ivy/common-run/bc*-jdk18on-*.jar
```

Connect to `https://www.bouncycastle.org/download/bouncy-castle-java-fips/#latest` and download the latest versions of the base (`bc-fips`), PKIX (`bcpkix-fips`) and TLS (`bctls-fips`) cryptography providers. At the time of writing, these are:

```
bc-fips-1.0.2.5.jar
bcpkix-fips-1.0.7.jar
bctls-fips-1.0.19.jar
```

Newer versions of these libraries should work but have not been tested by Dataiku.

Copy those 3 jars in the `lib/ivy/common-run/` directory of the DSS kit.


## 5. Configure the new JDK

Choose a directory name `<DSS_JDK_DIR>` which will hold the custom Java runtime (e.g. `/usr/local/dss-java11`) and populate it with the following command:

```sh
jlink \
	--add-modules "$(java --list-modules | sed 's/@.*/,/' | tr -d '\n')" \
	--ignore-signing-information \
	--output <DSS_JDK_DIR>
```

replacing `<DSS_JDK_DIR>` with the location you have chosen for the new JDK to create. The latter should not exist (it will be created and populated by this command), and this command should preferably run as root so the target JDK is owned by the superuser account.

Note that `java` and `jlink` in the above should of course refer to the system-provided JDK11 versions of these programs. Prefix them with full path if needed
(typically: `/usr/lib/jvm/java-11-openjdk/bin`).

Note also that you will need to regenerate this custom JDK using the same command after an update of the system-provided one, in order to propagate the changes
provided by this update.


Edit the security configuration file of the newly-created Java runtime, located at `<DSS_JDK_DIR>/conf/security/java.security` (as root):

- Locate the block of lines configuring the FIPS-mode security providers (`fips.provider.N`) and replace it with:
```
fips.provider.1=org.bouncycastle.jcajce.provider.BouncyCastleFipsProvider
fips.provider.2=org.bouncycastle.jsse.provider.BouncyCastleJsseProvider fips:BCFIPS
fips.provider.3=SUN
fips.provider.4=SunEC
fips.provider.5=com.sun.net.ssl.internal.ssl.Provider BCFIPS
```
- Locate the definitions for the following four keys, and configure them as follows:
```
keystore.type=jks
fips.keystore.type=PKCS12
security.useSystemPropertiesFile=true
ssl.KeyManagerFactory.algorithm=PKIX
```

Replace file `<DSS_JDK_DIR>/lib/security/cacerts` in the new JDK with a link to `/etc/pki/java/cacerts` (OS-maintained system-wide certificate trust store).


## 6. DSS installation

You can now install and run DSS following the standard procedure, making sure it uses the Java runtime which you have configured above.

For this, you need to make sure the JAVA_HOME environment variable is defined to point to it, as in:
```
export JAVA_HOME=<DSS_JDK_DIR>
```


This should be the case for DSS installation as well as startup scripts. You can for example define this variable in the session initialization file for the DSS Linux user account, eg `$HOME/.bash_profile` or equivalent.

### Setup the OpenSAML java option

Edit the file in the data directory `<DATA_DIR>/bin/env-default.sh` and add the following line at the end:

```sh
export DKU_JAVA_OPTS="$DKU_JAVA_OPTS -Dopensaml.config.ecdh.defaultKDF=PBKDF2"
```

This step ensures that the default key derivation function used by OpenSAML’s ECDH operations is set to PBKDF2, which is necessary for FIPS compliance. Make sure to restart DSS after making these changes to apply the new configuration.

Restart DSS which should be now FIPS compliant.