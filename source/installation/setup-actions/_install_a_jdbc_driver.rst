Install a JDBC driver
---------------------

Instances come pre-configured with drivers for PostgresSQL, MariaDB, Snowflake, AWS Athena and Google BigQuery. If you need another driver, this setup action eases the process. It can download a file by HTTP, HTTPS, from S3 bucket or from an ABS container.

.. list-table:: Install JDBC Driver parameters
   :widths: 20 80
   :header-rows: 1

   * - Parameter
     - Expected value
   * - Database type
     - | The type of database you will use.
       | This parameter has no actual effect, it is used for readability.
   * - URL
     - | This field expects the full address to the driver file or archive.
       |  
       | Download from HTTP(S) endpoint:

       .. code-block:: bash

          http(s)://hostname/path/to/file.(jar|tar.gz|zip)

       | Redirections are solved before download.
       |
       | Download from a S3 bucket:

       .. code-block:: bash

          s3://BUCKET_NAME/OBJECT_NAME

       | Download from Azure Blob Storage:

       .. code-block:: bash

          abs://STORAGE_ACCOUNT_NAME/CONTAINER_NAME/OBJECT_NAME

       | Use a driver available on the machine:

       .. code-block:: bash

          file://path/to/file.(jar|tar.gz|zip)
   * - Paths in archive
     - | This field must be used when the driver is shipped as a tarball or a ZIP file.
       | Add here all the paths to find the JAR files in the driver archive.
       | Paths are relative to the top of the archive. Wildcards are supported.
       | Examples of paths:

       .. code-block:: bash

          *.jar

       .. code-block:: bash

          subdirA/*.jar
          subdirB/*.jar


   * - HTTP Headers
     - List of HTTP headers to add to the query. One header per line.

       .. code-block:: text

          Header1: Value1
          Header2: Value2

       Parameter ignored for all other kinds of download.

   * - HTTP Username
     - | **HTTP**
       |
       | If the endpoint expect Basic Authentication, use this parameter to specify the
       | user name.
       |
       | **Azure**
       |
       | If the instance have several Managed Identities, set the *client_id* of the
       | targeted one in this parameter.
       |
       | To connect to Azure Blob Storage with a SAS Token (not recommended), set the
       | value of this parameter to *token*.
   * - HTTP Password
     - | **HTTP**
       |
       | If the endpoint expect Basic Authentication, use this parameter to specify the
       | password.
       |
       | **Azure**
       |
       | To connect to Azure Blob Storage with a SAS Token (not recommended), store the
       | token value in this parameter.
   * - Datadir subdirectory
     - For very specific use-cases only, we recommend to let it empty.
