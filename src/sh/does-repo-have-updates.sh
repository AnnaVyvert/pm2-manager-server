#!/bin/bash
source $1

cd $RFHSCR_PROJECT_PATH

OUT_=$(git fetch --dry-run)
OUT2_=$(git status)

FETCH_UPDATES_=$(echo $OUT_ | grep "remote:")
DETACHED_=$(echo $OUT2_ | grep "detached")

echo $FETCH_UPDATES_ $DETACHED_

if [ $FETCH_UPDATES_ ] || [ $DETACHED_ ]
then 
  echo "YES";
else
  echo "NOT";
fi