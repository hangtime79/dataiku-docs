# HOWTO: Make a custom Basic credentials provider for a SQL connection

Write code like:

```
package com.customer.dataiku.mycredentials;

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

import com.dataiku.dip.connections.DSSConnection;
import com.dataiku.dip.connections.AbstractSQLConnection.CustomDatabaseProperty;
import com.dataiku.dip.connections.DSSConnection.BasicConnectionCredentialProvider;
import com.dataiku.dip.security.model.ICredentialsService.BasicCredential;
import com.dataiku.dip.security.AuthCtx;
import com.google.gson.Gson;
import com.google.gson.JsonObject;

public class MyCredentialsProvider implements BasicConnectionCredentialProvider {
    private DSSConnection conn;
    private Map<String, String> providerParams = new HashMap<>();

    @Override
    public void setConnection(DSSConnection conn) {
        this.conn = conn;
        logger.info("Setting connection for provider: " + conn.name);
    }

    @Override
    public void setParams(List<CustomDatabaseProperty> params) {
        for (CustomDatabaseProperty c : params) {
            logger.info("Setting provider param: " + c.name + "=" + c.value);
            providerParams.put(c.name, c.value);
        }
    }

    @Override
    public BasicCredential getCredential(AuthCtx authCtx) {
        logger.info("Acquiring credential for DSS user: " + authCtx.getIdentifier());
        try {
            /* Sample: call a "vaultURL" to retrieve tokens. In order to call the vaultURL,
             * we must retrieve a "vaultKey" from a file on disk */
            String vaultKey = FileUtils.readFileToString(new File("/home/dataiku/vault.key"), 
                                                                    StandardCharsets.UTF_8);

            String queryString =  URLEncoder.encode("targetUser", "UTF-8") + "=" + 
                                  URLEncoder.encode(authCtx.getIdentifier(), "UTF-8");
            URL vaultURL = new URL(providerParams.get("vaultURL") + "?" + queryString);
            HttpURLConnection urlConn = (HttpURLConnection) vaultURL.openConnection();
            urlConn.setRequestMethod("GET");

            urlConn.setRequestProperty("X-API-Key", vaultKey.trim());

            int status = urlConn.getResponseCode();

            if (status != 200) {
                /* Currently, only unchecked exceptions are supported - they will be catched anyway */
                throw new IllegalArgumentException("Failed to acquire credentials, status " + status);
            }

            JsonObject response = new Gson().fromJson(new InputStreamReader(urlConn.getInputStream(),
                                                            StandardCharsets.UTF_8), JsonObject.class);

            String login = response.get("login").getAsString();
            String password = response.get("password").getAsString();

            return new BasicCredential(login, password);
        } catch (IOException e) {
            throw new IllegalArgumentException("Failed to acquire credentials", e);
        }

    }

    private static final Logger logger = Logger.getLogger("com.customer.dataiku.mycredentials");
}
```

Compile this class, linking against:

* `INSTALLDIR/lib/ivy/common-run/*`
* `INSTALLDIR/lib/ivy/backend-run/*`
* `INSTALLDIR/dist/*`

Package it to a jar, and place the resulting jar in `DATADIR/java`

Restart DSS

Configure the connection with:

* Credentials mode: Global (even if your code provides per-user credentials)
* Credentials > Custom provider (advanced):`com.customer.dataiku.mycredentials.MyCredentialsProvider`
* Custom provider settings:
  * vaultURL -> Your URL

Save and test. In case of errors during test, errors can be found in `DATADIR/run/backend.log`

*Warning*: These instructions are provided as-is, as custom credentials provider is an experimental advanced option. The API may change in a future DSS release.