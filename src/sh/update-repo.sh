#!/bin/bash
source $1

cd $RFHSCR_PROJECT_PATH

git pull --ff origin main

echo "YES"