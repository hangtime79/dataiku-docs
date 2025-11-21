Glue metastore 
###############

This kind of metastore catalog is the preferred setup when running on AWS and when using managed AWS services like EMR, EKS or Athena.

To enable Glue metastore, go to Admin > Settings > Metastore catalogs and select "AWS Glue".

For authentication, we strongly recommend to use authentication through a S3 connection.

* Create a S3 connection
* Set Glue Auth to "Use AWS credentials from a connection"
* Enter your S3 connection name

This way, all access to the Glue metastore will be done through the (possibly per-user) credentials defined in the S3 connection. When submitting Spark jobs, DSS will automatically configure Spark to use Glue with the appropriate credential.

