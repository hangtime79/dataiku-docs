#!/bin/bash -e
MYDIR=$(cd "$(dirname "$0")" && pwd -P)
BRANCH=$1
if [ -z "$BRANCH" ]; then
    BRANCH=master
fi
echo "Fetching Python code from branch $BRANCH..."
rm -rf $MYDIR/dataiku/
svn export https://github.com/dataiku/dip/branches/$BRANCH/src/main/python/dataiku/ dataiku
