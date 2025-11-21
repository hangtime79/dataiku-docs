#! /bin/sh -e

MYDIR=`dirname $0`
MYDIR=`cd $MYDIR && pwd -P`
ROOTDIR=`cd $MYDIR/.. && pwd -P`

MAJOR_VERSION=14

DTKDEVADM_BASE=/data/dtkdevadm

REFDOC_DIR=$DTKDEVADM_BASE/www/doc.dataiku.com/htdocs
REFDOC_BACKUP=$DTKDEVADM_BASE/www/doc.dataiku.com/backup/`date +%Y-%m-%d-%H-%M-%S`

DEVGUIDE_DIR=$DTKDEVADM_BASE/www/developer.dataiku.com/htdocs
DEVGUIDE_BACKUP=$DTKDEVADM_BASE/www/developer.dataiku.com/backup/`date +%Y-%m-%d-%H-%M-%S`

export SPARK_DIR=$DTKDEVADM_BASE/api-doc-build/dataiku-dss-spark-standalone-13.5.5-3.5.3-generic-hadoop3/
export API_DOC_BUILD_DIR=$DTKDEVADM_BASE/api-doc-build/$MAJOR_VERSION

export OSS_NOTICE_BUILD_DIR="$DTKDEVADM_BASE/oss-notice-build/$MAJOR_VERSION"
export OSS_NOTICE_LAUNCHER_BUILD_DIR="$DTKDEVADM_BASE/oss-notice-build/launcher/"
export OSS_NOTICE_STORIES_BUILD_DIR="$DTKDEVADM_BASE/oss-notice-build/stories/$MAJOR_VERSION"
export OSS_NOTICE_CLOUD_BUILD_DIR="$DTKDEVADM_BASE/oss-notice-build/cloud/"


echo "Building Third party licenses"
(
	cd $ROOTDIR
	DKUINSTALLDIR="$OSS_NOTICE_BUILD_DIR" DKUGETITSTARTEDDIR="$OSS_NOTICE_CLOUD_BUILD_DIR" DSSLAUNCHERDIR="$OSS_NOTICE_LAUNCHER_BUILD_DIR" DSSSTORIESDIR="$OSS_NOTICE_STORIES_BUILD_DIR" make update-licenses
)

echo "Third party licenses built"

echo "Building Refdoc HTML"
(
	cd $ROOTDIR
	export PYTHONPATH=$ROOTDIR/python:$API_DOC_BUILD_DIR/internal-python/:$API_DOC_BUILD_DIR/internal-python-lambda/:$SPARK_DIR/python:$SPARK_DIR/python/lib/py4j-0.10.7-src.zip
	make clean
	sphinx-build -b dkuhtml -j auto source build/html
)
echo "Refdoc HTML Built"


echo "Building app notes"
(
	cd $ROOTDIR
	cd app-notes && make clean all
)
echo "App notes built"

echo "Building Developer guide HTML"
(
	cd $ROOTDIR/developer-guide
	export PYTHONPATH=$ROOTDIR/python:$API_DOC_BUILD_DIR/internal-python/:$API_DOC_BUILD_DIR/internal-python-lambda/:$SPARK_DIR/python:$SPARK_DIR/python/lib/py4j-0.10.7-src.zip
	make clean
	sphinx-build -j auto source build/html
)

echo "Backing up refdoc"
(
	mkdir -p $REFDOC_BACKUP
	set +e
	mv $REFDOC_DIR/dss/$MAJOR_VERSION/* $REFDOC_BACKUP
	set -e
)
echo "Refdoc Backup done"

echo "Deploying ref doc"
(
	mkdir -p $REFDOC_DIR/dss/$MAJOR_VERSION
	cp -r $ROOTDIR/build/html/* $REFDOC_DIR/dss/$MAJOR_VERSION
)
echo "Ref doc deployed"


echo "Backing up devguide"
(
	mkdir -p $DEVGUIDE_BACKUP
	set +e
	mv $DEVGUIDE_DIR/$MAJOR_VERSION/* $DEVGUIDE_BACKUP
	set -e
)
echo "devguide Backup done"

echo "Deploying devguide"
(
	mkdir -p $DEVGUIDE_DIR/$MAJOR_VERSION
	cp -r $ROOTDIR/developer-guide/build/html/* $DEVGUIDE_DIR/$MAJOR_VERSION
)
echo "devguide deployed"

echo "Backing up appnotes"
(
	if [ -f $REFDOC_DIR/app-notes/ ]
	then
		mkdir -p $REFDOC_BACKUP/app-notes
		mv $REFDOC_DIR/app-notes/$MAJOR_VERSION $REFDOC_BACKUP/app-notes/$MAJOR_VERSION
	fi
)
echo "appnotes backup done"


echo "Deploying app notes"
(
	mkdir -p $REFDOC_DIR/app-notes/$MAJOR_VERSION
	cp -r $ROOTDIR/app-notes/build/* $REFDOC_DIR/app-notes/$MAJOR_VERSION
)
echo "App notes deployed"

#cp $ROOTDIR/.htaccess $REFDOC_DIR
cp $ROOTDIR/source/troubleshooting/errors/.htaccess $REFDOC_DIR/dss/$MAJOR_VERSION/troubleshooting/errors
cp $ROOTDIR/robots.txt $REFDOC_DIR
echo "DONE"
