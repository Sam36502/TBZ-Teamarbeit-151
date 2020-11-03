#!/bin/bash

echo Starting Annales Memum MySQL Container...

sudo docker kill bismarck6502/annales-memum-db
sudo docker rm bismarck6502/annales-memum-db
sudo docker run -d -p 3306:3306 --name annales-memum-db \
	-e MYSQL_ROOT_PASSWORD=4nn_m3m \
	bismarck6502/annales-memum-db

echo Done!
