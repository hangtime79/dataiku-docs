Using reverse proxies
######################

.. contents::
    :local:

If you want to expose DSS to your users on a different host and/or port than its native installation, you need
  to configure a reverse proxy in front of DSS. This is the case in particular if you want to expose DSS on the
  standard HTTP/80 or HTTPS/443 ports, as DSS should not run with superuser privileges.


The following configuration snippets can be adapted to forward Data Science Studio interface through an external nginx or Apache web server,
to accomodate deployments where users should access it through a different base URL than that of its native host and port installation
(for example to expose Data Science Studio on the standard HTTP port 80, or on a different host name).

.. warning::

    Data Science Studio does not currently support being remapped to a base URL with a non-empty path prefix
    (that is, to ``http://HOST:PORT/PREFIX/`` where ``PREFIX`` is not empty).


HTTP deployment behind a nginx reverse proxy
===============================================

.. code-block:: nginx

    # nginx reverse proxy configuration for Dataiku Data Science Studio
    # requires nginx version 1.4 or above
    server {
        # Host/port on which to expose Data Science Studio to users
        listen 80;
        server_name dss.example.com;
        location / {
            # Base url of the Data Science Studio installation
            proxy_pass http://DSS_HOST:DSS_PORT/;
            proxy_redirect off;
            # Allow long queries
            proxy_read_timeout 3600;
            proxy_send_timeout 600;
            # Allow large uploads
            client_max_body_size 0;
            # Allow large downloads
            proxy_max_temp_file_size 0;
            # Allow protocol upgrade to websocket
            proxy_http_version 1.1;
            proxy_set_header Host $http_host;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }
    }

HTTPS deployment behind a nginx reverse proxy
===============================================

DSS can also be accessed using secure HTTPS connections, provided you have a valid certificate for the host name on which it should be visible
(some browsers do not accept secure WebSocket connections using untrusted certificates).

You can configure this by deploying a nginx reverse proxy server, on the same or another host than Data Science Studio,
using a variant of the following configuration snippet:

.. code-block:: nginx

    # nginx SSL reverse proxy configuration for Dataiku Data Science Studio
    # requires nginx version 1.4 or above
    server {
        # Host/port on which to expose Data Science Studio to users
        listen 443 ssl;
        server_name dss.example.com;
        ssl_certificate /etc/nginx/ssl/dss_server_cert.pem;
        ssl_certificate_key /etc/nginx/ssl/dss_server.key;
        location / {
            # Base url of the Data Science Studio installation
            proxy_pass http://DSS_HOST:DSS_PORT/;
            proxy_redirect http://$proxy_host https://$host;
            proxy_redirect http://$host https://$host;
            # Allow long queries
            proxy_read_timeout 3600;
            proxy_send_timeout 600;
            # Allow large uploads
            client_max_body_size 0;
            # Allow large downloads
            proxy_max_temp_file_size 0;
            # Allow protocol upgrade to websocket
            proxy_http_version 1.1;
            proxy_set_header Host $http_host;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }
    }

.. note::
  If all DSS users access it over HTTPS, you can enforce session cookies security as described in :doc:`/security/advanced-options`.


HTTP deployment behind an Apache reverse proxy
===============================================

The following configuration snippet can be used to forward DSS through an Apache HTTP server:

.. code-block:: apache

    # Apache reverse proxy configuration for Dataiku Data Science Studio
    # requires Apache version 2.4.5 or above
    LoadModule proxy_module modules/mod_proxy.so
    LoadModule proxy_http_module modules/mod_proxy_http.so
    LoadModule proxy_wstunnel_module modules/mod_proxy_wstunnel.so
    LoadModule rewrite_module modules/mod_rewrite.so

    <VirtualHost *:80>
        ServerName dss.example.com
        RewriteEngine On
        RewriteCond %{HTTP:Connection} Upgrade [NC]
        RewriteCond %{HTTP:Upgrade} WebSocket [NC]
        RewriteRule /(.*) ws://DSS_HOST:DSS_PORT/$1 [P]
        RewriteRule /(.*) http://DSS_HOST:DSS_PORT/$1 [P]
        ProxyPassReverse / http://DSS_HOST:DSS_PORT/
        ProxyPreserveHost on
        ProxyTimeout 3600
    </VirtualHost>
