#!/usr/bin/env bash -e

function usage {
    echo >&2
    echo "Usage: $0 [-h] [-d dip_dir | -b branch] destination" >&2
    echo 'Builds the doc for DSS Spark public API and moves it to <destination>.' >&2
    echo '<destination>'\''s parent directory must exist and be writable.' >&2
    echo >&2
    echo 'Options:' >&2
    echo '  -h          Displays this message and exits' >&2
    echo '  -d dip_dir  Build the doc from this dip directory. If unspecified, checkout from git.' >&2
    echo '  -b branch   Set the branch to checkout. Disables -d. Defaults to current dss-doc branch.' >&2
    echo >&2
    echo 'Example:' >&2
    echo "  $0 -d ../dip ./scala"
}

# Option parsing
BRANCH=
DIP_DIR=
while getopts :b:d:h opt; do
    case $opt in
        b)
            BRANCH="$OPTARG"
            DIP_DIR=
            ;;
        d)
            if [ -z "$BRANCH" ]; then
                if [ ! -d "$OPTARG"/dss-spark-public ]; then
                    echo "$OPTARG"'/dss-spark-public/ does not exist' >&2
                    exit 2
                fi
                DIP_DIR=$(cd "$OPTARG" && pwd -P)
            fi
            ;;
        h)
            usage
            exit 0
            ;;
        \?)
            echo "Invalid option: -$OPTARG" >&2
            usage
            exit 1
            ;;
        :)
            echo "Option -$OPTARG requires an argument." >&2
            usage
            exit 1
            ;;
    esac
done
shift $((OPTIND-1))
if [ -z "$1" ]; then
    echo "Destination argument is required" >&2
    usage
    exit 1
elif [ -e "$1" ]; then
    echo "Destination already exists" >&2
    file "$1"
    exit 2
fi
DEST_NAME=$(basename "$1")
DEST_PARENT=$(cd "$(dirname "$1")" && pwd -P)
if [ ! -d "$DEST_PARENT" ]; then
    echo "$DEST_PARENT is not writable"
    exit 2
fi


# Temp dir & cleanup
MYDIR=$(cd "$(dirname "$0")" && pwd -P)
function cleanup() {
    rm -rf tmp-spark-build
    popd >/dev/null
}
function err_report() {
    echo "Error on line $1" >&2
}
pushd $MYDIR >/dev/null
mkdir tmp-spark-build
trap cleanup EXIT
trap 'err_report $LINENO' ERR

# Checkout from git
if [ -z "$DIP_DIR" ]; then
    DIP_DIR=tmp-spark-build/dip

    if [ -z "$BRANCH" ]; then
        BRANCH=`git rev-parse --abbrev-ref HEAD`
    fi

    # Lightweight partial ("sparse") checkout
    mkdir "$DIP_DIR"
    cd "$DIP_DIR"
    git init
    git config core.sparseCheckout true
    echo '/dss-spark-public' > .git/info/sparse-checkout
    git remote add origin ssh://git@github.com/dataiku/dip.git
    git pull origin "$BRANCH" --depth 1
    # Required jars to build doc
    mkdir -p ./lib/ivy/spark-build_2.10/
    for pack in core sql catalyst; do
        mvn dependency:get dependency:copy -Dartifact=org.apache.spark:spark-"$pack"_2.10:1.5.2:jar -Dtransitive=false -DoutputDirectory=lib/ivy/spark-build_2.10
    done
    cd "$MYDIR"
fi

# Build doc
(cd "$DIP_DIR"/dss-spark-public && sbt doc)
mv "$DIP_DIR"/dss-spark-public/target/scala-2.10/api "$DEST_PARENT/$DEST_NAME"

