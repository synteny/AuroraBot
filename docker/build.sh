#!/bin/bash

cp ../sessioncontroller/db.sql dockerfiles/mysql

docker build -t app dockerfiles/app/
docker build -t data dockerfiles/data/
docker build -t db dockerfiles/mysql/
