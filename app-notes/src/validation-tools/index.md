# Dataiku DSS validation tools

Starting with version 12.5.2, DSS provides two validation tools to verify the integrity and proper behavior of a DSS instance.

These tools can assist you in qualifying the proper use of DSS software and support the required qualification processes.

## Installation validation

The installation validation tool verifies that the software is properly installed according to expected specifications. The main function of the installation validation tool is to verify the integrity of each file against the original Dataiku manufactured version. It also performs additional consistency checks on the installation integrity.

### Requirements

The installation validation tool is designed to run on Cloud Stacks instances. It can also run on Custom instances that have a fully functioning pandoc installation, including the ability to build PDF reports (which requires a LaTeX installation).

In order to download the checksum verification file, the installation validation tool requires outgoing Internet connectivity. Specifically, it will connect to `https://cdn.downloads.dataiku.com/`.

### Running 

To run the installation validation tool, go to the DSS data directory, and run:

```
./bin/dssadmin verify-installation-integrity
```

The installation validation tool downloads the checksum file, performs the file integrity check, and additional checks. It runs in a few minutes

Once the validation tool has run, it produces a summary report, such as:


```
Finished
Verification report has been output in /data/dataiku/dss_data/verification-report.pdf
Verification overall status is PASSED
```

If the overall status is PASSED, the validation was successful.

### Report

You can review the `verification-report.pdf` file that is produced in the DSS data directory

If the validation is not successful, we recommend opening a Dataiku Support ticket. Please see <https://doc.dataiku.com/dss/latest/troubleshooting/obtaining-support.html>


## Operational validation

The operational validation tool is a self-test project that runs various calculations and recipes and verifies that their output is correct.

The main function of the operational validation tool is to ensure that the running instance of Dataiku DSS operates as expected.

### Requirements

The operational validation tool requires a Dataiku instance with a Filesystem (local) connection.

The operational validation tool is designed to run on Cloud Stacks instances. It can also run on Custom instances, provided that:

* Graphics export feature is installed
* They have a fully functioning pandoc installation, including the ability to build PDF reports (which requires a LaTeX installation).

### Downloading the operational validation project

Download the project from the following location:

```
https://cdn.downloads.dataiku.com/public/validation-tools/DSS_OPERATIONAL_VALIDATION_1_0_0.zip
```

### Importing

Import the project in your Dataiku instance. If you have Filesystem connections with non-default names, you will need to remap them

### Running

Follow the instructions in the project home page for running the validation

### Report

After running, the tool produces several outputs, one of which is the `operational-validation-report.pdf`.

It contains both an overall status and the tests that were run.

If the validation is not successful, we recommend opening a Dataiku Support ticket. Please see <https://doc.dataiku.com/dss/latest/troubleshooting/obtaining-support.html>