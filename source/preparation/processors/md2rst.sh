#! /bin/sh

MYDIR=`dirname $0`
MYDIR=`cd $MYDIR && pwd -P`

TMPDIR=$MYDIR/tmp

cd $TMPDIR
for f in *md
do
	f=`echo $f|sed 's,.md,,'`
	existing="$MYDIR/${f}.rst"

	pandoc --from=markdown --to=rst --output=tmp.rst $f.md
	cat tmp.rst|sed 's,TITLE:\(.*\),\1\n#############################################,g' > $f.rst

	rm -f $f.md

	echo "\n\n.. pristine" >> $f.rst

	if test -f $existing
	then
		if grep -q ".. pristine" $existing
		then
			echo "[+] $f already exists and is pristine, overriding it" >&2
			mv $f.rst $MYDIR
		else
			echo "[+] $f already exists but MODIFIED, ignoring" >&2
		fi
	else
		echo "[+] $f doesn't exist yet" >&2
		mv $f.rst $MYDIR
	fi
	echo "        $f"
done
