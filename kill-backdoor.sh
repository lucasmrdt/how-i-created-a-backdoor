#!/usr/bin/env bash

kill -9 `ps aux | grep -v $0 | grep backdoor | tr -s ' ' | cut -d ' ' -f2` 2> /dev/null
