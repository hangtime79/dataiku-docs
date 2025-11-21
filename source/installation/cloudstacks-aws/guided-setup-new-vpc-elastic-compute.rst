Guided setup 1: Deploy in a new VPC with Elastic Compute
########################################################

.. contents::
   :local:


Description
===========

This guided setup allows you to setup a full Dataiku Cloud Stacks for AWS setup, including the ability to run workloads on Elastic Compute clusters powered by Kubernetes (using Amazon EKS).

At the end of this setup, you'll have:

* A fully-managed DSS design node, with either a public IP or a private one
* The ability to one-click create elastic compute clusters
* The elastic compute clusters running with public IPs (and no NAT gateway overhead)


Prerequisites
=============

You need to have administrative access to an existing AWS subscription

Steps
=====

VPC setup
---------

In the AWS console, go to the *VPC* service

* Create a new VPC. Select a /16 CIDR, for example ``10.0.0.0/16``. In the rest of this document, the id of this VPC will be noted as ``vpc-id``

* Right-click on the VPC, and select "Edit VPC settings", enable the option "Enable DNS hostnames" and save. Check that "Enable DNS resolution" is also enabled

* Inside the VPC, create two subnets in different availability zones, each with a /20 CIDR. For example ``10.0.0.0/20`` and ``10.0.16.0/20``. In the rest of this document, the id of these subnets will be noted as ``subnet1-id`` and ``subnet2-id``

* For each of ``subnet1-id`` and ``subnet2-id``, right-click on it, select "Edit subnet settings" and tick the box to "Enable auto-assign public IPv4 address". Then "Save"

* Create an Internet Gateway and attach it to ``vpc-id``

* Edit the main route table of ``vpc-id``, and add a new route:

* Destination: ``0.0.0.0/0``
* Target: select "Internet gateway", then the Internet gateway that you just created

Your new network is now setup and ready to receive a Dataiku Cloud Stacks setup

IAM setup
---------

In the AWS console, go to the *IAM* service


Role for DSS
%%%%%%%%%%%%

* Click on "Roles", then on "Create role"

* In "Type of trusted entity", select "AWS service" and click on "EC2"

* Click on "Next" (Add permissions) and on "Next" (Name, review, and create)

* Give a name to the role. In the rest of this document, this role name will be noted as ``dss-role-name``

* Click on the role, click on "Add permissions", then on "Attach policies" and select the following policies:

* ``AmazonEC2FullAccess``
* ``AWSCloudFormationFullAccess``

* Click on "Attach policy"

* Click on "Add permissions" and then on "Create inline policy"

* In the policy editor, click on the JSON tab and enter this policy. In the whole JSON, replace ``<account_id>`` by your AWS account id

.. code-block:: json

    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": [
                    "ecr:CreateRepository",
                    "ecr:BatchGetImage",
                    "ecr:CompleteLayerUpload",
                    "ecr:DescribeImages",
                    "ecr:TagResource",
                    "ecr:GetAuthorizationToken",
                    "ecr:DescribeRepositories",
                    "ecr:UploadLayerPart",
                    "ecr:InitiateLayerUpload",
                    "ecr:BatchCheckLayerAvailability",
                    "ecr:PutImage",
                    "kms:CreateGrant",
                    "kms:DescribeKey",
                    "eks:*",
                    "secretsmanager:*"
                ],
                "Resource": "*"
            },
            {
                "Effect": "Allow",
                "Action": [
                    "ssm:GetParameter",
                    "ssm:GetParameters"
                ],
                "Resource": [
                    "arn:aws:ssm:*:<account_id>:parameter/aws/*",
                    "arn:aws:ssm:*::parameter/aws/*"
                ]
            },
            {
                "Effect": "Allow",
                "Action": [
                    "iam:CreateInstanceProfile",
                    "iam:DeleteInstanceProfile",
                    "iam:GetInstanceProfile",
                    "iam:ListInstanceProfiles",
                    "iam:AddRoleToInstanceProfile",
                    "iam:ListInstanceProfilesForRole",
                    "iam:RemoveRoleFromInstanceProfile",
                    "iam:GetRole",
                    "iam:CreateRole",
                    "iam:DeleteRole",
                    "iam:AttachRolePolicy",
                    "iam:PutRolePolicy",
                    "iam:PassRole",
                    "iam:DetachRolePolicy",
                    "iam:DeleteRolePolicy",
                    "iam:GetRolePolicy",
                    "iam:GetOpenIDConnectProvider",
                    "iam:CreateOpenIDConnectProvider",
                    "iam:DeleteOpenIDConnectProvider",
                    "iam:ListAttachedRolePolicies",
                    "iam:TagRole"
                ],
                "Resource": [
                    "arn:aws:iam::<account_id>:instance-profile/eksctl-*",
                    "arn:aws:iam::<account_id>:role/eksctl-*",
                    "arn:aws:iam::<account_id>:oidc-provider/*",
                    "arn:aws:iam::<account_id>:role/aws-service-role/eks-nodegroup.amazonaws.com/AWSServiceRoleForAmazonEKSNodeGroup",
                    "arn:aws:iam::<account_id>:role/eksctl-managed-*"
                ]
            },
            {
                "Effect": "Allow",
                "Action": [
                    "iam:GetRole"
                ],
                "Resource": [
                    "arn:aws:iam::<account_id>:role/*"
                ]
            },
            {
                "Effect": "Allow",
                "Action": [
                    "iam:CreateServiceLinkedRole"
                ],
                "Resource": "*",
                "Condition": {
                    "StringEquals": {
                        "iam:AWSServiceName": [
                            "eks.amazonaws.com",
                            "eks-nodegroup.amazonaws.com",
                            "eks-fargate.amazonaws.com"
                        ]
                    }
                }
            },
            {
                "Sid": "EKSAutoScalingWrite",
                "Effect": "Allow",
                "Action": [
                    "autoscaling:UpdateAutoScalingGroup",
                    "autoscaling:DeleteAutoScalingGroup",
                    "autoscaling:CreateAutoScalingGroup"
                ],
                "Resource": [
                    "arn:aws:autoscaling:*:*:autoScalingGroup:*:autoScalingGroupName/*"
                ]
            },
            {
                "Sid": "EKSAutoScalingRead",
                "Effect": "Allow",
                "Action": [
                    "autoscaling:DescribeAutoScalingGroups",
                    "autoscaling:DescribeScalingActivities",
                    "autoscaling:DescribeLaunchConfigurations"
                ],
                "Resource": "*"
            }
        ]
    }

* Click on "Review Policy", then on "Create policy"

* Take note of the "Instance profile ARN". In the rest of this document, it will be noted as ``dss-role-instance-profile-arn``

* Take note of the "Role ARN". In the rest of this document, it will be noted as ``dss-role-arn``


Role for Fleet Manager
%%%%%%%%%%%%%%%%%%%%%%

* Click on Roles, then on Create role

* In "Type of trusted entity", select "AWS service" and click on "EC2"

* Click on "Next" (Add permissions) and on "Next" (Name, review, and create)

* Give a name to the role. In the rest of this document, this role name will be noted as ``fm-role-name``

* Click on the role, click on "Add permissions", then on "Create inline policy"

* In the policy editor, click on the JSON tab and enter this policy. In the whole JSON, replace ``<dss-role-arn>`` by the role ARN you noted earlier

.. code-block:: json

    {
    "Version": "2012-10-17",
    "Statement": [
        {
        "Effect": "Allow",
        "Action": [
            "ec2:DeleteVolume",
            "ec2:StartInstances",
            "ec2:StopInstances",
            "ec2:AttachVolume",
            "ec2:ModifyVolume",
            "ec2:DeleteSnapshot",
            "ec2:RebootInstances",
            "ec2:TerminateInstances",
            "ec2:AssociateIamInstanceProfile",
            "ec2:DisassociateIamInstanceProfile",
            "ec2:CreateTags",
            "ec2:DeleteSecurityGroup",
            "ec2:AuthorizeSecurityGroupIngress",
            "ec2:CreateVolume",
            "ec2:CreateTags",
            "ec2:DescribeVpcs",
            "ec2:DescribeSubnets",
            "ec2:DescribeVolumes",
            "ec2:DescribeInstances",
            "ec2:DescribeIamInstanceProfileAssociations",
            "ec2:DescribeSecurityGroups",
            "ec2:CreateSecurityGroup",
            "ec2:RunInstances",
            "ec2:CreateSnapshot",
            "ec2:AssociateAddress",
            "ec2:CreateRoute",
            "ec2:DeleteRoute",
            "ec2:DescribeRouteTables",
            "ec2:AcceptVpcPeeringConnection",
            "ec2:DeleteVpcPeeringConnection",
            "ec2:CreateVpcPeeringConnection",
            "ec2:DescribeVpcPeeringConnections",
            "sts:GetCallerIdentity",
            "sts:AssumeRole",
            "route53:ChangeResourceRecordSets",
            "route53:ListResourceRecordSets",
            "route53:GetChange",
            "acm:DescribeCertificate",
            "acm:ExportCertificate",
            "acm:ListCertificates",
            "acm:RenewCertificate",
            "acm:DeleteCertificate",
            "acm:UpdateCertificateOptions",
            "elasticloadbalancing:*"
        ],
        "Resource": [
            "*"
        ]
        },
        {
        "Effect": "Allow",
        "Action": "iam:PassRole",
        "Resource": "<dss-role-arn>"
        }
    ]
    }

* Click on "Review policy", enter a policy name and click on "Create policy"

Fleet Manager setup
-------------------

In the AWS console, go to the *CloudFormation* service

* Click on "Create stack" and then "With new resources"

* In "Amazon S3 URL", enter ``https://dataiku-cloudstacks.s3.amazonaws.com/templates/fleet-manager/14.2.2/fleet-manager-instance.yml``

.. note::

    This template creates an IAM role to setup a daily backup policy. An alternative template without role creation (nor backup policy) is available at ``https://dataiku-cloudstacks.s3.amazonaws.com/templates/fleet-manager/14.2.2/fleet-manager-instance-no-dlm.yml``

* Click on "Next"

* Enter a name for your deployment

* In "VPC Id", enter ``vpc-id``

* In "Subnet Id", enter ``subnet1-id``

* In "IP addresses allowed to connect to Fleet Manager", either enter ``0.0.0.0/0`` to authorize TCP connection to Fleet Manager from anywhere, or enter the CIDR corresponding to your own IP address range (w.x.y.z/32)

* In "SSH KeyPair", select an existing keypair that will be able to connect to Fleet Manager (it is not normally required)

* In "Fleet Manager IAM role", enter ``fm-role-name``

* In "Fleet Manager password", enter a strong password. This is the password that you'll need to manage your Dataiku Cloud Stacks fleet

* Click on "Next"

* Optionally, you can add tags that you would like to be propagated to the deploying resources then click again on "Next"

* At the bottom, check the "I acknowledge that AWS CloudFormation might create IAM resources with custom names."

* Click on "Create Stack"

* Wait for your stack to appear as "CREATE_COMPLETE"

* In the "Resources" tab of the stack, click on the "Instance" entry

* Copy the "Public IPv4 address"

This is the address at which your Cloud Stacks Fleet manager is deployed. Open a new tab to this address.

Start your first DSS
--------------------

* Log into Fleet Manager with "admin" as the login, and the password you previously entered

* In "Cloud Setup", click on "Enter license" and enter your Dataiku license. Save

* Refresh the page in your browser

* In "Fleet Blueprints", click on "DEPLOY ELASTIC DESIGN", give a name to your new fleet and in "Instance profile ARN", enter the ``dss-role-instance-profile-arn``

* Click on "Deploy"

* Go to "Instances > All", click on the design node

* Click "Provision"

* Wait for your DSS instance to be ready

* Click on "Retrieve password" and write-down the password

* Click on "Go to DSS"

* Login with "admin" as the login, and the password you just retrieved

You can now start using DSS

(Optional) Start your first Elastic compute cluster
---------------------------------------------------

* In Fleet Manager, go to your Virtual Network, and note the id of the "Default security group". In the rest of the document, this will be noted as ``defaultsg-id``

* In DSS, go to "Administration > Clusters"

* Click on "Create EKS cluster", give it a name

* In "Connection", enter your region name

* In "Network settings", set to "Manually defined"

* In "VPC subnets", enter ``subnet1-id``, then Enter, then ``subnet2-id``, then Enter

* In "Security groups", enter ``defaultsg-id``, then Enter

* In "Initial node pool", set to "Manually defined"

* Click on "Start"

* Wait for your cluster to be available

* In "Settings", go to "Containerized execution", and in "Default cluster", select the cluster you just created

* In a project, you can now use containerized execution for any activity, using the ``eks-default`` containerized config
