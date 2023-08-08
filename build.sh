#!/bin/bash

docker build . -t cat_data_watcher:latest -f Dockerfile
# docker image tag cat_data_watcher:latest registry.meanderingtech.corp/software/cat_data_watcher:latest 

