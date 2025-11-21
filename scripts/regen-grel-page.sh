#! /bin/sh -e

MYDIR=`dirname $0`
MYDIR=`cd $MYDIR && pwd -P`
ROOTDIR=`cd $MYDIR/.. && pwd -P`

if [ -z "$BACKEND_PORT" ]; then
    BACKEND_PORT=8082
fi

JSONFILE="$ROOTDIR/build/grel.json"
RSTFILE="$ROOTDIR/source/advanced/formula.rst.INTEGRATE_ME"

echo "Fetching GREL function definitions from DSS http://localhost/:$BACKEND_PORT... into $JSONFILE"

curl "http://localhost:$BACKEND_PORT/dip/api/shaker/get-expression-syntax" >$JSONFILE

echo "Producing page $RSTFILE"

python regen-grel-page.py $JSONFILE $RSTFILE

