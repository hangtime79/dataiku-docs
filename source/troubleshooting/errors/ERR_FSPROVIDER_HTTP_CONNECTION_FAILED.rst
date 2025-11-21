ERR_FSPROVIDER_HTTP_CONNECTION_FAILED: HTTP connection failed
##########################################################################

DSS tried to connect to a HTTP server but couldn't establish the connection.

This error can happen:

* when trying to preview or use HTTP datasets
* when trying to run a download recipe with HTTP sources

This error indicates that the connection could not be established.
The message of the error will contain additional information.

Some common reasons for failure to establish the connection are:

* The connection settings (host, port, ...) to the server are invalid
* The HTTP server is not running or not accepting connections
* There is a firewall blocking connection attempts from DSS to the HTTP server
* The URL is incorrectly labeled as HTTPS instead of HTTP or vice-versa


Remediation
===========

The first step for solving this issue is to go to the dataset's or download recipe
settings screen.

* Refer to the :doc:`documentation on HTTP dataset </connecting/http>` and
  :doc:`documentation on DSS and Hive </other_recipes/download>`
  in order to get additional information on HTTP sources in DSS.
* Make sure that the URLs are correct
* Try accessing these URLs in the browser
* Try accessing these URLs using the ``curl`` command line from the DSS server
* Check if a firewall is blocking connections between DSS and the HTTP server(s)
