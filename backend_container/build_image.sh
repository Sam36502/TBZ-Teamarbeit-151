#!/bin/bash

echo Building Annales-Memum Application Image...

sudo docker build -t bismarck6502/annales-memum-app:latest .

echo Pushing New Build to Dockerhub...

sudo docker push bismarck6502/annales-memum-app

echo Done!
