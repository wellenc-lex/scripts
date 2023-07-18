#!/bin/bash

# get all running docker container names
containers=$(docker images --format {{.Repository}}:{{.Tag}})
id=0

# loop through all containers
for container in $containers
do
  id=$((id+1))
  echo "Container: $container, ID=$id"
  runsecrets=$(docker run -it --rm --name=deepfence-secretscanner -v $(pwd):/home/deepfence/output -v /var/run/docker.sock:/var/run/docker.sock deepfenceio/deepfence_secret_scanner:latest -image-name $container  --json-filename $id.json)
done