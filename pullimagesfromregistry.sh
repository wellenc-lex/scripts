#!/bin/sh

REGISTRY="IP:port"

for repo in $(curl -s http://$REGISTRY/v2/_catalog | jq -r '.repositories[]') ; do
    for tag in $(curl -s http://$REGISTRY/v2/$repo/tags/list | jq -r '.tags[]') ; do
        docker pull $REGISTRY/$repo:$tag
	echo $REGISTRY/$repo:$tag
    done
done
