#!/bin/bash

export PG_LOG_DIR=/var/log/amp/amp-geocoder-pg
export PROJ=geocoder

docker-compose -p $PROJ down