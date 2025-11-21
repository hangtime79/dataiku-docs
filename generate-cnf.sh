#!/bin/bash

rm -rf notice-data
python ./scripts/dep_json_rst.py --format cnf -o notice-data \
	-i ./source/thirdparty-elems/frontend.json -i ./source/thirdparty-elems/frontend-manual-dependencies.json \
	-i ./source/thirdparty-elems/java.json -i ./source/thirdparty-elems/java-manual-dependencies.json \
	-i ./source/thirdparty-elems/python.json \
	-i ./source/thirdparty-elems/data.json \
	-i ./source/thirdparty-elems/native.json \
	-i ./source/thirdparty-elems/r.json \
	-i ./source/thirdparty-elems/scala.json

zip dataiku-dss-thirdparty-notice.zip -r notice-data -j
