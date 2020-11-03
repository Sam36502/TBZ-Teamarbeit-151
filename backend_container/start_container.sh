#!/bin/bash

echo Starting Annales-Memum Application...
echo   make sure the database container is started as well.

sudo docker kill annales-memum-app
sudo docker rm annales-memum-app
sudo docker run -d -p 5000:80 --name annales-memum-app bismarck6502/annales-memum-app

echo done!
