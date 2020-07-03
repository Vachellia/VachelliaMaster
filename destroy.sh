#!/bin/bash

echo "stopping vm ..."
# stop vm
docker container stop vm

echo "removing vm ..."
# remove vm
docker container rm vm