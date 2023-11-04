#!/bin/bash
source $1

BE_PROCESS_ID=$(pm2 status | grep "$RFHSCR_BE_PROCESS_NAME" | awk '{print $2}')
FE_PROCESS_ID=$(pm2 status | grep "$RFHSCR_FE_PROCESS_NAME" | awk '{print $2}')

pm2 stop $BE_PROCESS_ID $FE_PROCESS_ID

echo "YES"