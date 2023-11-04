#!/bin/bash
source $1

BE_PROCESS_ID=$(pm2 status | grep $RFHSCR_BE_PROCESS_NAME | awk '{print $2}')
FE_PROCESS_ID=$(pm2 status | grep $RFHSCR_FE_PROCESS_NAME | awk '{print $2}')

if [[ -z "$BE_PROCESS_ID" || -z "$FE_PROCESS_ID" ]]; then
  echo "no processes with such names"
  exit 1
fi

pm2 restart $BE_PROCESS_ID

sleep "$RFHSCR_BE_BUILD_COOLDOWN"s

pm2 restart $FE_PROCESS_ID

sleep "$RFHSCR_FE_BUILD_COOLDOWN"s

echo "YES"