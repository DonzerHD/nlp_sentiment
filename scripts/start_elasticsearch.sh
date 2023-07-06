#!/bin/bash
docker run -d -p 9200:9200 --name elastic -e "discovery.type=single-node" -v $(pwd)/data:/usr/share/elasticsearch/data --memory=2g --cpus=2 docker.elastic.co/elasticsearch/elasticsearch:7.17.10
