#!/bin/bash

if [ -z ${DKUINSTALLDIR} ]
then
    echo "DKUINSTALLDIR is not set, set it before calling this script"
    exit 1
fi

if [ -z ${DSSLAUNCHERDIR} ]
then
    echo "DSSLAUNCHERDIR is not set, set it before calling this script"
    exit 1
fi

if [ -z ${DSSSTORIESDIR} ]
then
    echo "DSSSTORIESDIR is not set, set it before calling this script"
    exit 1
fi

if [ -z ${DKUGETITSTARTEDDIR} ]
then
    echo "DKUGETITSTARTEDDIR is not set, set it before calling this script"
    exit 1
fi

python3 ./scripts/dep_json_rst.py -i "${DKUINSTALLDIR}/licenses/notice/data/frontend.json" -i "${DKUINSTALLDIR}/licenses/notice/data/frontend-manual.json" -d "${DKUINSTALLDIR}/licenses/notice/license_texts" -o ./source/thirdparty-elems/frontend.rst
python3 ./scripts/dep_json_rst.py -i "${DKUINSTALLDIR}/licenses/notice/data/java.json" -i "${DKUINSTALLDIR}/licenses/notice/data/java-manual.json" -d "${DKUINSTALLDIR}/licenses/notice/license_texts" -o ./source/thirdparty-elems/java.rst
python3 ./scripts/dep_json_rst.py -i "${DKUINSTALLDIR}/licenses/notice/data/python.json" -d "${DKUINSTALLDIR}/licenses/notice/license_texts" -o ./source/thirdparty-elems/python.rst
python3 ./scripts/dep_json_rst.py -i "${DKUINSTALLDIR}/licenses/notice/data/data.json" -d "${DKUINSTALLDIR}/licenses/notice/license_texts" -o ./source/thirdparty-elems/data.rst
python3 ./scripts/dep_json_rst.py -i "${DKUINSTALLDIR}/licenses/notice/data/r.json" -d "${DKUINSTALLDIR}/licenses/notice/license_texts" -o ./source/thirdparty-elems/r.rst
python3 ./scripts/dep_json_rst.py -i "${DKUINSTALLDIR}/licenses/notice/data/scala.json" -d "${DKUINSTALLDIR}/licenses/notice/license_texts" -o ./source/thirdparty-elems/scala.rst
python3 ./scripts/dep_json_rst.py -i "${DSSLAUNCHERDIR}/licenses/notice/data/launcher.json" -d "${DSSLAUNCHERDIR}/licenses/notice/license_texts" -o ./source/thirdparty-elems/launcher.rst
python3 ./scripts/dep_json_rst.py -i "${DKUINSTALLDIR}/licenses/notice/data/fm-frontend.json" -d "${DKUINSTALLDIR}/licenses/notice/license_texts" -o ./source/thirdparty-elems/fm-frontend.rst
python3 ./scripts/dep_json_rst.py -i "${DKUINSTALLDIR}/licenses/notice/data/fm-java.json" -d "${DKUINSTALLDIR}/licenses/notice/license_texts" -o ./source/thirdparty-elems/fm-java.rst
python3 ./scripts/dep_json_rst.py -i "${DSSSTORIESDIR}/licenses/notice/data/story.json" -i "${DSSSTORIESDIR}/licenses/notice/data/story-manual.json" -d "${DSSSTORIESDIR}/licenses/notice/license_texts" -o ./source/thirdparty-elems/story.rst
python3 ./scripts/dep_json_rst.py -i "${DKUGETITSTARTEDDIR}/licenses/notice/data/console-frontend.json" -d "${DKUGETITSTARTEDDIR}/licenses/notice/license_texts" -o ./source/thirdparty-elems/cloud-frontend.rst
python3 ./scripts/dep_json_rst.py -i "${DKUGETITSTARTEDDIR}/licenses/notice/data/java-drivers-manual.json" -d "${DKUGETITSTARTEDDIR}/licenses/notice/license_texts" -o ./source/thirdparty-elems/cloud-java-drivers.rst
python3 ./scripts/dep_json_rst.py -i "${DKUGETITSTARTEDDIR}/licenses/notice/data/python-manual.json" -d "${DKUGETITSTARTEDDIR}/licenses/notice/license_texts" -o ./source/thirdparty-elems/cloud-python.rst

# Extract for GCP third parties aknowledgements: https://github.com/dataiku/dku-automation/blob/master/community-edition/ce-gcp/roles/dss/files/thirdparty.rst
python3 scripts/dependency_gcp_merge.py

#solutions licenses
python3 ./scripts/dep_json_rst.py -i "solutions/SOL_BATCH_PERF_OPTIM-v0.1.0-frontend.json" -o source/thirdparty-elems/solutions/SOL_BATCH_PERF_OPTIM-frontend.rst
python3 ./scripts/dep_json_rst.py -i "solutions/SOL_CLAIM_MODELING-v1.0.3-python-merged.json" -o source/thirdparty-elems/solutions/SOL_CLAIM_MODELING-python.rst
python3 ./scripts/dep_json_rst.py -i "solutions/SOL_CLV_FORECAST-v1.2.0-python-merged.json" -o source/thirdparty-elems/solutions/SOL_CLV_FORECAST-python.rst
python3 ./scripts/dep_json_rst.py -i "solutions/SOL_CREDIT_RISK_STRESS_TESTING-v1.1.0-python-merged.json" -o source/thirdparty-elems/solutions/SOL_CREDIT_RISK_STRESS_TESTING-python.rst
python3 ./scripts/dep_json_rst.py -i "solutions/SOL_CREDIT_SCORING-v1.1.1-python-merged.json" -o source/thirdparty-elems/solutions/SOL_CREDIT_SCORING-python.rst
python3 ./scripts/dep_json_rst.py -i "solutions/SOL_CS_INTEL-v1.2.1-frontend.json" -o source/thirdparty-elems/solutions/SOL_CS_INTEL-frontend.rst
python3 ./scripts/dep_json_rst.py -i "solutions/SOL_CS_INTEL-v1.2.1-python-merged.json" -o source/thirdparty-elems/solutions/SOL_CS_INTEL-python.rst
python3 ./scripts/dep_json_rst.py -i "solutions/SOL_CUST_REVIEWS_ANALYSIS-v2.0.0-python-merged.json" -o source/thirdparty-elems/solutions/SOL_CUST_REVIEWS_ANALYSIS-python.rst
python3 ./scripts/dep_json_rst.py -i "solutions/SOL_DEMAND_FORECAST-v2.0.0-python-merged.json" -o source/thirdparty-elems/solutions/SOL_DEMAND_FORECAST-python.rst
python3 ./scripts/dep_json_rst.py -i "solutions/SOL_DIST_RETAIL-v1.1.0-python.json" -o source/thirdparty-elems/solutions/SOL_DIST_RETAIL-python.rst
python3 ./scripts/dep_json_rst.py -i "solutions/SOL_FACTORIES_FORECAST-v1.1.1-python.json" -o source/thirdparty-elems/solutions/SOL_FACTORIES_FORECAST-python.rst
python3 ./scripts/dep_json_rst.py -i "solutions/SOL_MARKDOWN_OPTIMIZATION-v2.0.0-frontend.json" -o source/thirdparty-elems/solutions/SOL_MARKDOWN_OPTIMIZATION-frontend.rst
python3 ./scripts/dep_json_rst.py -i "solutions/SOL_MARKDOWN_OPTIMIZATION-v2.0.0-python-merged.json" -o source/thirdparty-elems/solutions/SOL_MARKDOWN_OPTIMIZATION-python.rst
python3 ./scripts/dep_json_rst.py -i "solutions/SOL_MBA-v1.1.7-python-merged.json" -o source/thirdparty-elems/solutions/SOL_MBA-python.rst
python3 ./scripts/dep_json_rst.py -i "solutions/SOL_MNT_PERF_PLAN-v2.1.1-python-merged.json" -o source/thirdparty-elems/solutions/SOL_MNT_PERF_PLAN-python.rst
python3 ./scripts/dep_json_rst.py -i "solutions/SOL_MOL_PROP_PRED-v1.1.0-python-merged.json" -o source/thirdparty-elems/solutions/SOL_MOL_PROP_PRED-python.rst
python3 ./scripts/dep_json_rst.py -i "solutions/SOL_PROCESS_MINING-v1.4.1-frontend.json" -o source/thirdparty-elems/solutions/SOL_PROCESS_MINING-frontend.rst
python3 ./scripts/dep_json_rst.py -i "solutions/SOL_PROCESS_MINING-v1.4.1-python-merged.json" -o source/thirdparty-elems/solutions/SOL_PROCESS_MINING-python.rst
python3 ./scripts/dep_json_rst.py -i "solutions/SOL_PRODUCT_RECO-v2.1.4-frontend.json" -o source/thirdparty-elems/solutions/SOL_PRODUCT_RECO-frontend.rst
python3 ./scripts/dep_json_rst.py -i "solutions/SOL_PRODUCT_RECO-v2.1.4-python-merged.json" -o source/thirdparty-elems/solutions/SOL_PRODUCT_RECO-python.rst
python3 ./scripts/dep_json_rst.py -i "solutions/SOL_REAL_ESTATE_PRICING-v1.0.4-python-merged.json" -o source/thirdparty-elems/solutions/SOL_REAL_ESTATE_PRICING-python.rst
python3 ./scripts/dep_json_rst.py -i "solutions/SOL_RECONCILIATION-v1.0.2-frontend.json" -o source/thirdparty-elems/solutions/SOL_RECONCILIATION-frontend.rst
python3 ./scripts/dep_json_rst.py -i "solutions/SOL_SDOH-v2.1.0-frontend.json" -o source/thirdparty-elems/solutions/SOL_SDOH-frontend.rst
python3 ./scripts/dep_json_rst.py -i "solutions/SOL_SDOH-v2.1.0-python-merged.json" -o source/thirdparty-elems/solutions/SOL_SDOH-python.rst