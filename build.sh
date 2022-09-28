#!/bin/bash

docker build . -t cat_data_watcher:latest -f docker/Dockerfile
# docker image tag cat_data_watcher:latest registry.kernel.corp/software/test_station_watcher:latest 
# the image will be stored somewhere locally
# Lets see if we can use that image in docker-compose.yml  