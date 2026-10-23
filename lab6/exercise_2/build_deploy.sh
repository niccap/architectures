#!/bin/bash

docker build -f car_dockerfile -t niccap/car_inventory .
docker build -f vin_dockerfile -t niccap/vin_decoder .
docker push niccap/car_inventory
docker push niccap/vin_decoder
kubectl apply -f car_inventory.yaml -f vin_decoder.yaml 
