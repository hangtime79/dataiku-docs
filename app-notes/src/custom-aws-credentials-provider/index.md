# HOWTO: Make a custom AWS credentials provider

Write code like:

```
package com.dataiku.dip.connections;

import java.io.File;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
import java.net.URLEncoder;
import java.nio.charset.StandardCharsets;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import org.apache.commons.io.FileUtils;
import org.apache.log4j.Logger;

import com.dataiku.dip.connections.AbstractSQLConnection.CustomDatabaseProperty;
import com.dataiku.dip.connections.ConnectionWithAWSAuthCredentials;
import com.dataiku.dip.connections.ConnectionWithAWSAuthCredentials.AWSConnectionCredentialsProvider;
import com.dataiku.dip.connections.ConnectionWithAWSAuthCredentials.SerializableAWSCredential;
import com.dataiku.dip.security.AuthCtx;
import com.google.gson.Gson;
import com.google.gson.JsonObject;

public class MyCredentialsProvider implements AWSConnectionCredentialsProvider {
    private ConnectionWithAWSAuthCredentials conn;
    private Map<String, String> providerParams = new HashMap<>();

    @Override
    public void setConnection(ConnectionWithAWSAuthCredentials conn) {
        this.conn = conn;
        logger.info("Setting connection for provider");
    }

    @Override
    public void setParams(List<CustomDatabaseProperty> params) {
        for (CustomDatabaseProperty c : params) {
            logger.info("Setting provider param: " + c.name + "=" + c.value);
            providerParams.put(c.name, c.value);
        }
    }

    @Override
    public SerializableAWSCredential get(AuthCtx authCtx) {
        logger.info("Acquiring credential for DSS user: " + authCtx.getIdentifier());
        try {
            /* Sample: call a "vaultURL" to retrieve tokens */
            String queryString =  URLEncoder.encode("targetUser", "UTF-8") + "=" +  URLEncoder.encode(authCtx.getIdentifier(), "UTF-8");

            URL vaultURL = new URL(providerParams.get("vaultURL") + "?" + queryString);
            HttpURLConnection urlConn = (HttpURLConnection) vaultURL.openConnection();
            urlConn.setRequestMethod("GET");

            /* In this sample, we read the authentication to the vault from a file on disk */
            String vaultKey = FileUtils.readFileToString(new File("/home/dataiku/vault.key"), StandardCharsets.UTF_8);

            urlConn.setRequestProperty("X-API-Key", vaultKey.trim());

            int status = urlConn.getResponseCode();

            if (status != 200) {
                /* Currently, only unchecked exceptions are supported - they will be catched anyway */
                throw new IllegalArgumentException("Failed to acquire credentials, status " + status);
            }

            JsonObject response = new Gson().fromJson(new InputStreamReader(urlConn.getInputStream(), StandardCharsets.UTF_8), JsonObject.class);

            String accessKey = response.get("accessKey").getAsString();
            String secretKey = response.get("accessKey").getAsString();
            /* Only if it's a STS */
            String sessionToken = response.get("sessionToken").getAsString();

            return new SerializableAWSCredential(accessKey, secretKey, sessionToken);
        } catch (IOException e) {
            throw new IllegalArgumentException("Failed to acquire credentials", e);
        }

    }

    private static final Logger logger = Logger.getLogger("dku.credentials.aws.mine");
}
```

Compile this class, linking against:

* `INSTALLDIR/lib/ivy/common-run/*`
* `INSTALLDIR/lib/ivy/backend-run/*`
* `INSTALLDIR/dist/*`

Package it to a jar, and place the resulting jar in `DATADIR/java`

Restart DSS

Configure the connection with:

* Credentials: Custom
* Custom provider class: `com.dataiku.dip.connections.MyCredentialsProvider`
* Custom provider settings:
  * vaultURL -> Your URL
  * Don't forget to click "Add"

Save and test. In case of errors during test, errors can be found in `DATADIR/run/backend.log`

*Warning*: These instructions are provided as-is, as custom credentials provider is an experimental advanced option. The API may change in a future DSS release.