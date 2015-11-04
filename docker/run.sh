#!/bin/bash

if [ -z ${TELEGRAM_TOKEN+x} ]; then echo "TELEGRAM_TOKEN environment variable is not defined. Set it to the bot token."; exit 1; fi

./stop.sh

docker rm app
docker rm db
docker rm data
docker rm rabbitmq

docker run --name data data

docker run --name db \
        --volumes-from data \
        -e MYSQL_USER=aurorabot \
        -e MYSQL_PASSWORD=12345 \
        -v `pwd`/etc/mysql/conf.d:/etc/mysql/conf.d \
        -d db

docker run --name rabbitmq \
	-d rabbitmq:3

docker run --name app \
	--link rabbitmq \
	--link db \
	-e TELEGRAM_TOKEN=$TELEGRAM_TOKEN \
        -v `pwd`/..:/var/aurorabot \
	app \
        sh /var/aurorabot/docker/entrypoint.sh
