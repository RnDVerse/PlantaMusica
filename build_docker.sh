#!/bin/bash


docker build . -t "plantamusica"

docker tag plantamusica dreambrooktech/plantamusica:v0.1.3

docker push dreambrooktech/plantamusica:v0.1.3

