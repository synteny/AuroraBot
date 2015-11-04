#!/bin/bash

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
	-e TELEGRAM_TOKEN=161743683:AAHhg4I1bIJveXWEo8AzYkV0WBs1OwI19G0 \
        -v `pwd`/..:/var/aurorabot \
	app \
        sh /var/aurorabot/docker/entrypoint.sh
