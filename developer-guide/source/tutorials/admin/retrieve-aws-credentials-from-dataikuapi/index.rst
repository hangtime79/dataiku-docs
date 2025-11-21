Retrieve AWS Credentials from Dataiku API
*****************************************

Prerequisites
#############

* A machine running Dataiku


Introduction 
#############

You may have the need to manage users permission for security and organization purposes. 
In Dataiku, it is possible to manage AWS permissions through code with the Python API.
With these credentials, it is then possible to manage AWS resources. 


Connecting AWS and Dataiku
###########################

Before being able to retrieve AWS credentials for Dataiku resources you must:

1. Ensure that the machine running Dataiku has an `IAM instance profile <https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_use_switch-role-ec2_instance-profiles.html>`_.
2. Enable a S3 connection with `AssumeRole <https://docs.aws.amazon.com/STS/latest/APIReference/API_AssumeRole.html>`_ mode and **Details readable by** parameter. See more on `this tutorial <https://knowledge.dataiku.com/latest/admin-configuring/connection-security/tutorial-aws-assumerole-mechanism.html>`_. 
3. As the role to assume, use ``${adminProperty:associatedRole}``.
4. In each user’s settings, in **Admin Properties**, add an entry ``associatedRole`` with the name of the IAM role to assume.
5. Ensure that the IAM instance profile of the machine running Dataiku can assume the needed roles.


Retrieving
###########

The following code allows you to retrieve AWS credentials with a Dataiku API call and the S3 connection previously enabled. 

.. tabs::

    .. group-tab:: In Dataiku

        .. code-block:: python
            :linenos:
            :name: retrieving_aws_credentials

            import dataiku

            # to complete as needed
            MY_S3_CONNECTION = ""
    
            conn_info = dataiku.api_client().get_connection(MY_S3_CONNECTION).get_info()
            cred = conn_info.get_aws_credential()


    .. group-tab:: Outside Dataiku

        .. code-block:: python
            :linenos:

            import dataiku

            # to complete as needed
            MY_S3_CONNECTION = ""
            DATAIKU_HOST = ""
            MY_API_KEY = ""

            dataiku.set_remote_dss(f"http://{DATAIKU_HOST}", API_KEY)
    
            conn_info = dataiku.api_client().get_connection(MY_S3_CONNECTION).get_info()
            cred = conn_info.get_aws_credential()

The output ``cred`` is a dict that contains the Security Token Service (STS) token.
 
.. note::

    If you run your code on an API endpoint, such as Kubernetes,
    you will have to initialize the Dataiku API client with :meth:`dataikuapi.DSSClient()` prior the steps described above.

This dictionary also contains access and secret keys, which allows to manage AWS resources.
You can do it with `boto3 <https://boto3.amazonaws.com/v1/documentation/api/latest/index.html>`_, 
which is the AWS Software Development Kit (SDK) to access AWS services.

As an example, the code below allows you to create a session and access your `S3 buckets <https://docs.aws.amazon.com/s3/>`_. 

.. code-block:: python
    :linenos:

    import boto3

    # Create a session using the retrieved credentials
    session = boto3.Session(
        aws_access_key_id=cred['accessKey'],
        aws_secret_access_key=cred['secretKey'],
        aws_session_token=cred['sessionToken']
    )

    # Use the session to interact with AWS services, such as S3 for example
    s3 = session.client('s3')

    # Example: List all buckets in S3
    response = s3.list_buckets()


Wrapping up
#############

In this tutorial, you retrieved credentials to manage AWS resources on a machine running Dataiku. 