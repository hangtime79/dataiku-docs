Add Certificate Authority to DSS truststore
-------------------------------------------

This setup action is a convenient way to add a Certificate Authority to your DSS instances' truststore. It will then be trusted for Java, R and Python processes.
It takes a Certificate Authority in the public PEM format. A chain of trust can also be added by appending all the certificates in the same setup action.

Example (single CA):

.. code-block::

  -----BEGIN CERTIFICATE-----
  (Your Root certificate authority)
  -----END CERTIFICATE-----

Example (Chain of Trust):

.. code-block::

  -----BEGIN CERTIFICATE-----
  (Your Primary SSL certificate)
  -----END CERTIFICATE-----
  -----BEGIN CERTIFICATE-----
  (Your Intermediate certificate)
  -----END CERTIFICATE-----
  -----BEGIN CERTIFICATE-----
  (Your Root certificate authority)
  -----END CERTIFICATE-----


.. warning::

    The name must be unique for each CA as it is used to write the CA in your instances.
