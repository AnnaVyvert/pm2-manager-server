#!/bin/bash
source $1

cd $RFHSCR_PROJECT_PATH

git pull --ff origin $2

echo "YES"