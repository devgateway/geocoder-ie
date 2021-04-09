#!/bin/bash

# remove any unused networks
docker network prune -f

# create and assign correct owner for pg_log directory
export PG_LOG_DIR=/var/log/amp/amp-geocoder-pg
mkdir -p $PG_LOG_DIR
chmod 777 $PG_LOG_DIR

export PROJ=geocoder
export TMPDIR=$(pwd)

# start amp
docker-compose -p $PROJ up -d --force-recreate