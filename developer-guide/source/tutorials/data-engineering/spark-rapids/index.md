# Using Spark RAPIDS on Dataiku

## Overview

This guide provides step-by-step instructions for setting up and configuring the **RAPIDS Accelerator for Apache Spark** (i.e., Spark RAPIDS) with **Dataiku** on an **Amazon EKS** cluster with GPU support. The setup enables GPU acceleration for Spark workloads, significantly improving performance for compatible operations.

:::{note}
This guide assumes familiarity with Dataiku administration, Docker, and basic Kubernetes concepts.

You'll need administrative access to your Dataiku instance and AWS environment.
:::

## Prerequisites

- Access to AWS with permissions to create and manage EKS clusters
- Dataiku instance with administrative access
- Docker installed and configured
- SSH access to your Dataiku instance

## EKS Cluster Setup

### Requirements
- EKS cluster with **NVIDIA GPU** support
- Example instance types:
  - P4d EC2 instances
  - G4 EC2 instances

### Setup Instructions
1. Follow the [Dataiku EKS Cluster Setup Guide](https://doc.dataiku.com/dss/latest/containers/eks/index.html) for initial cluster creation.

2. Ensure NVIDIA GPU support is properly configured in your cluster.

## Building a Custom Spark Docker Image with RAPIDS

### Accessing the Dataiku Instance
1. SSH into your Dataiku instance using the Terminal:
   ```bash
   ssh <user>@<your-instance-address>
   ```
   :::{note}
   If you do not already have access, download `wget` using the command ```sudo yum install wget``` before proceeding to the next step.
   :::

2. Sudo to the dataiku user and switch to the Dataiku user home directory (`/data/dataiku`)
   ```bash
   sudo -su dataiku
   ```


### Downloading Required Files
3. Download the RAPIDS jar file:
   
   ```bash
   wget https://repo1.maven.org/maven2/com/nvidia/rapids-4-spark_2.12/25.02.0/rapids-4-spark_2.12-25.02.0.jar
   ```
   :::{note}
   The link for the latest RAPIDS jar can be found at [Download | spark-rapids](https://nvidia.github.io/spark-rapids/docs/download.html)
   :::

4. Download the GPU discovery script:

   ```bash
   wget -O getGpusResources.sh https://raw.githubusercontent.com/apache/spark/master/examples/src/main/scripts/getGpusResources.sh
   ```

### File Configuration
5. Move the Rapids jar to the Dataiku Spark directory:

   ```bash
   cp rapids-4-spark_2.12-25.02.0.jar /opt/dataiku-dss-<YOUR VERSION>/spark-standalone-home/jars/
   ```

6. Move the GPU discovery script to the Dataiku Spark directory:

   ```bash
   cp getGpusResources.sh /opt/dataiku-dss-<YOUR VERSION>/spark-standalone-home/bin/
   ```

7. Make `getGpusResources.sh` executable:

   ```bash
   chmod +x /opt/dataiku-dss-<YOUR VERSION>/spark-standalone-home/bin/getGpusResources.sh
   ```

### Building the Docker Image
8. Build the custom Spark image with CUDA support:

   ```bash
   dss_data/bin/dssadmin build-base-image \
     --type spark \
     --without-r \
     --build-from-image nvidia/cuda:12.6.2-devel-rockylinux8 \
     --tag <add_a_unique_name>
   ```

## Dataiku Spark Configuration

### Creating a Custom Configuration
1. Navigate to the **Administration** panel in Dataiku.

2. Select **Settings** > **Spark** configurations.

3. Click the **+ ADD ANOTHER CONFIG** button.

### Configuration Settings
Configure the following settings:

| Setting | Value |
|---------|-------|
| Config name | `spark-rapids` |
| Config keys | `Default spark configs on the container` |
| Managed Spark-on-K8S | `Enabled` |
| Image registry URL | `<your-registry>/spark-rapids` |
| Image pre-push hook | `Enable push to ECR` |
| Kubernetes namespace | `default` |
| Authentication mode | `Create service accounts dynamically` |
| Base image | `<Replace with your image tag name from Step 2h>` |
| Managed cloud credentials | `Enabled` |
| Provide AWS credential | `From any AWS connection` | 

### Additional Parameters
Spark configuration parameters like these below can be used:

```properties
spark.rapids.sql.enabled=true
spark.rapids.sql.explain=NOT_ON_GPU
```
:::{note}
Additional properties can be found at [Configuration | spark-rapids](https://nvidia.github.io/spark-rapids/docs/configs.html).
:::

### Advanced Settings
Within **Advanced settings** > **Executor pod YAML** it is mandatory to include the GPU resource limits.
```properties
spec:
  containers:
  - resources:
      limits:
        nvidia.com/gpu: 1
```

### Pushing the Base Image
4. Click the **PUSH BASE IMAGES** button

## Congratulations!
You are now set up to begin using the Spark RAPIDS container.



## Best Practices

- Regularly update Rapids jar and Delta Core to maintain compatibility
- Monitor GPU utilization using NVIDIA tools
- Back up configurations before making changes
- Test the setup with a sample workload before production use

## Known Issues and Troubleshooting

### Missing GPU Resources Script
**Issue**: `getGpusResources.sh` file not found.

**Resolution**: 
```bash
wget https://raw.githubusercontent.com/apache/spark/master/examples/src/main/scripts/getGpusResources.sh
mv getGpusResources.sh /opt/dataiku/spark/conf/
chmod +x /opt/dataiku/spark/conf/getGpusResources.sh
```

### Delta Core ClassNotFoundException
**Issue**: Delta Core class not found during execution.

**Resolution**: 
1. Download the correct Delta Core JAR:
   ```bash
   wget https://repo1.maven.org/maven2/io/delta/delta-core_2.12/2.4.0/delta-core_2.12-2.4.0.jar
   ```
2. Move it to the Spark jars directory:
   ```bash
   mv delta-core_2.12-2.4.0.jar /opt/dataiku/spark/jars/
   ```

### Shim Loader Exception
**Issue**: Version mismatch in Shim Loader - ```java.lang.IllegalArgumentException: Could not find Spark Shim Loader for 3.4.1```

**Resolution**: Ensure compatibility between Rapids JAR and Spark versions

:::{important}
Always verify version compatibility between Spark, Rapids, and Delta Core components before deployment.
:::

### Spark Shuffle Manager
**Issue**:  
```text
RapidsShuffleManager class mismatch (com.nvidia.spark.rapids.spark340.RapidsShuffleManager !=
com.nvidia.spark.rapids.spark341.RapidsShuffleManager). Check that configuration
setting spark.shuffle.manager is correct for the Spark version being used.
```

**Resolution**: Ensure that the correct shuffle manager is configured for the Spark version you are using. Mappings can be found in the [RAPIDS Shuffle Manager](https://docs.nvidia.com/spark-rapids/user-guide/latest/additional-functionality/rapids-shuffle.html)

## Additional Resources

- [Dataiku Documentation](https://doc.dataiku.com/)
- [NVIDIA Spark RAPIDS Documentation](https://nvidia.github.io/spark-rapids/)
- [Apache Spark Documentation](https://spark.apache.org/docs/latest/)