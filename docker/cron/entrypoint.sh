#!/usr/bin/env bash
set -e

# start cron
cron

# tail log
tail -f /var/log/cron.log
