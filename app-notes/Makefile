all:
	mkdir -p build
	cp -r src/.htaccess build/
	rm -rf build/static && cp -r static/ build/

	# Create an edge node to a EMR cluster
	cp -r src/emr-edge-node build/
	(cd build/emr-edge-node && pandoc -s index.md -t html -o index.html --css ../static/pandoc.css)

	# Create an edge node to a HDInsight cluster
	cp -r src/hdinsight-edge-node build/
	(cd build/hdinsight-edge-node && pandoc -s index.md -t html -o index.html --css ../static/pandoc.css)

	# On-premise HA
	cp -r src/on-premise-ha build/
	(cd build/on-premise-ha && pandoc -s index.md -t html -o index.html --css ../static/pandoc.css)

	# AWS HA and DR
	cp -r src/aws-ha-dr build/
	(cd build/aws-ha-dr && pandoc -s index.md -t html -o index.html --css ../static/pandoc.css)

	# Azure HA and DR
	cp -r src/azure-ha-dr build/
	(cd build/azure-ha-dr && pandoc -s index.md -t html -o index.html --css ../static/pandoc.css)

	# Managing prod node
	cp -r src/managing-prod-dss-node build/
	(cd build/managing-prod-dss-node && pandoc -s index.md -t html -o index.html --css ../static/pandoc.css)

	# MapR MUS
	cp -r src/mapr-mus build/
	(cd build/mapr-mus && pandoc -s index.md -t html -o index.html --css ../static/pandoc.css)

	# Working with DSS behind URL filtering
	cp -r src/url-filtered-access build/
	(cd build/url-filtered-access && pandoc -s index.md -t html -o index.html --css ../static/pandoc.css)

	# MUS reference deployment: sentry ACLs
	cp -r src/mus-reference-deployment-sentry-acls build/
	(cd build/mus-reference-deployment-sentry-acls && pandoc -s index.md -t html -o index.html --css ../static/pandoc.css)

	# Microsoft R
	cp -r src/microsoft-r build/
	(cd build/microsoft-r && pandoc -s index.md -t html -o index.html --css ../static/pandoc.css)

	# Limiting uploads
	cp -r src/limiting-uploads build/
	(cd build/limiting-uploads && pandoc -s index.md -t html -o index.html --css ../static/pandoc.css)

	# Alation integration
	cp -r src/alation-integration build/
	(cd build/alation-integration && pandoc -s index.md -t html -o index.html --css ../static/pandoc.css)

	# Databricks integration on AWS
	cp -r src/databricks-aws build/
	(cd build/databricks-aws && pandoc -s index.md -t html -o index.html --css ../static/pandoc.css)

	# Azure Databricks integration
	cp -r src/databricks-azure build/
	(cd build/databricks-azure && pandoc -s index.md -t html -o index.html --css ../static/pandoc.css)

	# Alation integration
	cp -r src/emr-security build/
	(cd build/emr-security && pandoc -s index.md -t html -o index.html --css ../static/pandoc.css)

	# Spark-on-K8S-on-Azure
	cp -r src/spark-on-k8s-azure build/
	(cd build/spark-on-k8s-azure && pandoc -s index.md -t html -o index.html --css ../static/pandoc.css)

	# Spark-on-K8S-on-GCP
	cp -r src/spark-on-k8s-gcp build/
	(cd build/spark-on-k8s-gcp && pandoc -s index.md -t html -o index.html --css ../static/pandoc.css)

	# Create an edge node to a Dataproc cluster
	cp -r src/dataproc-edge-node build/
	(cd  build/dataproc-edge-node && pandoc -s index.md -t html -o index.html --css ../static/pandoc.css)

	# Custom AWS credentials
	cp -r src/custom-aws-credentials-provider build/
	(cd  build/custom-aws-credentials-provider && pandoc -s index.md -t html -o index.html --css ../static/pandoc.css)

	#  CIS benchmark
	cp -r src/cloudstacks-cis-benchmark build/
	(cd  build/cloudstacks-cis-benchmark && pandoc -s index.md -t html -o index.html --css ../static/pandoc.css)

	# Custom AWS credentials
	cp -r src/custom-basic-credentials-provider build/
	(cd  build/custom-basic-credentials-provider && pandoc -s index.md -t html -o index.html --css ../static/pandoc.css)

	# Custom File export postprocessing hook
	cp -r src/custom-file-export-postprocessing-hook build/
	(cd  build/custom-file-export-postprocessing-hook && pandoc -s index.md -t html -o index.html --css ../static/pandoc.css)

	# Port range limitation
	cp -r src/port-range-limitation build/
	(cd  build/port-range-limitation && pandoc -s index.md -t html -o index.html --css ../static/pandoc.css)

	# Connecting to Cloudera CDP Public Cloud Data Hub clusters
	cp -r src/cdp-public-cloud-integration build/
	(cd  build/cdp-public-cloud-integration && pandoc -s index.md -t html -o index.html --css ../static/pandoc.css)

	# Sublicenses without Cloud Stacks
	cp -r src/sublicenses-without-cloudstacks build/
	(cd  build/sublicenses-without-cloudstacks && pandoc -s index.md -t html -o index.html --css ../static/pandoc.css)

	# Connections/Projects restrictions plugin
	cp -r src/connections-projects-restrictions build/
	(cd  build/connections-projects-restrictions && pandoc -s index.md -t html -o index.html --css ../static/pandoc.css)

	# Cloud Stacks deprecated Python installation
	cp -r src/cloudstacks-deprecation-python-installation build/
	(cd  build/cloudstacks-deprecation-python-installation && pandoc -s --toc index.md -t html -o index.html --css ../static/pandoc.css)

	# Cloud Stacks manuall installation (without CFT...)
	cp -r src/cloudstacks-manual-fm-installation build/
	(cd  build/cloudstacks-manual-fm-installation && pandoc -s --toc index.md -t html -o index.html --css ../static/pandoc.css)

	# Deprecated Python support for code environments Docker images
	cp -r src/codeenvs-deprecatedpython-container build/
	(cd  build/codeenvs-deprecatedpython-container && pandoc -s --toc index.md -t html -o index.html --css ../static/pandoc.css)

	# Installing DSS on RHEL 8 with FIPS mode enabled (Java 8)
	cp -r src/fips-setup-rhel8-java8 build/
	(cd  build/fips-setup-rhel8-java8 && pandoc -s --toc index.md -t html -o index.html --css ../static/pandoc.css)

	# Installing DSS on RHEL 8 with FIPS mode enabled (Java 11)
	cp -r src/fips-setup-rhel8-java11 build/
	(cd  build/fips-setup-rhel8-java11 && pandoc -s --toc index.md -t html -o index.html --css ../static/pandoc.css)

	# Code environment resources: offline containers
	cp -r src/offline-container-code-env-resources build/
	(cd  build/offline-container-code-env-resources && pandoc -s --toc index.md -t html -o index.html --css ../static/pandoc.css)

	# Validation tools
	cp -r src/validation-tools build/
	(cd  build/validation-tools && pandoc -s --toc index.md -t html -o index.html --css ../static/pandoc.css)

	# Supported python version
	cp -r src/supported-python-versions build/
	(cd  build/supported-python-versions && pandoc -s --toc index.md -t html -o index.html --css ../static/pandoc.css)

	# OpenAI-compatible LLM APIs
	cp -r src/openai-compatible-llm-api build/
	(cd build/openai-compatible-llm-api && pandoc -s --toc index.md -t html -o index.html --css ../static/pandoc.css)

	# Secret fetchers
	cp -r src/secret-fetchers build/
	(cd  build/secret-fetchers && pandoc -s --toc index.md -t html -o index.html --css ../static/pandoc.css)

	# Hashed API keys
	cp -r src/enable-hashed-api-keys build/
	(cd  build/enable-hashed-api-keys && pandoc -s --toc index.md -t html -o index.html --css ../static/pandoc.css)

	# Serving scalable local LLM
	cp -r src/serve-scalable-local-llm build/
	(cd  build/serve-scalable-local-llm && pandoc -s --toc index.md -t html -o index.html --css ../static/pandoc.css)

	# Disaster Recovery with FM
	cp -r src/disaster-recovery-with-fleet-manager build/
	(cd  build/disaster-recovery-with-fleet-manager && pandoc -s --toc index.md -t html -o index.html --css ../static/pandoc.css)

	# Snowflake Cortex - Extended Integrations
	cp -r src/snowflake-cortex-extended-integrations build/
	(cd  build/snowflake-cortex-extended-integrations && pandoc -s --toc index.md -t html -o index.html --css ../static/pandoc.css)

	# Snowflake Optimizer
	cp -r src/snowflake-optimizer-native-app build/
	(cd  build/snowflake-optimizer-native-app && pandoc -s --toc index.md -t html -o index.html --css ../static/pandoc.css)

	# Transitioning from legacy to FY25 profiles (Fiscal year 2025)
	cp -r src/transitioning-from-legacy-to-fy25-profiles build/
	(cd build/transitioning-from-legacy-to-fy25-profiles && pandoc -s --toc index.md -t html -o index.html --css ../static/pandoc.css)

	# Auto Scaling Data Workloads
	cp -r src/autoscaling-data-workloads build/
	(cd  build/autoscaling-data-workloads && pandoc -s --toc index.md -t html -o index.html --css ../static/pandoc.css)

	# Examples of Scalable Deployments
	mkdir -p build/8tPHPicNeSAczCIyihNeh5yCpK4FB5/
	rsync -rv src/examples-of-scalable-deployments/ build/8tPHPicNeSAczCIyihNeh5yCpK4FB5/
	(cd build/8tPHPicNeSAczCIyihNeh5yCpK4FB5 && pandoc -s --toc index.md -t html -o index.html --css ../static/pandoc.css)

	# K8S security contexts
	cp -r src/k8s-security-context build/
	(cd  build/k8s-security-context && pandoc -s --toc index.md -t html -o index.html --css ../static/pandoc.css)


	# Implementing gitops for dataiku
	cp -r src/implementing-gitops-for-dataiku build/
	(cd  build/implementing-gitops-for-dataiku && pandoc -s --toc index.md -t html -o index.html --css ../static/pandoc.css)

	# Working with private marketplaces in Azure
	cp -r src/azure-private-marketplaces build/
	(cd build/azure-private-marketplaces && pandoc -s --toc index.md -t html -o index.html --css ../static/pandoc.css)

	# Advanced troubleshooting macro
	cp -r src/advanced-troubleshooting-macro build/
	(cd build/advanced-troubleshooting-macro && pandoc -s --toc index.md -t html -o index.html --css ../static/pandoc.css)

clean:
	rm -rf build
