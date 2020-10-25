#!/bin/bash

echo Starting Annales Memum MySQL Container...

sudo docker kill annales-memum-db
sudo docker rm annales-memum-db
sudo docker run -d -p 3306:3306 --name annales-memum-db \
	-e MYSQL_ROOT_PASSWORD=4nn_m3m \
	am-db
