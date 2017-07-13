#!/bin/bash
redis-cli SAVE
date=$(date +"%Y%m%d%H%M%S")
rm -rf /var/cp_redis_backup/*
cp /var/redis_backup/dump.rdb /var/cp_redis_backup/$date.rdb

echo "done"
