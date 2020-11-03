#!/bin/bash

echo Building Annales-Memum Database Image...

sudo docker build -t bismarck6502/annales-memum-db .

echo Pushing new Image to Dockerhub

sudo docker push bismarck6502/annales-memum-db

echo Done!
