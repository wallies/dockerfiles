#!/bin/bash
set -e
set -o pipefail

cd python-cuda
for file in Dockerfile-*; do
  echo "Building Dockerfile: $file"
  tag=${file#*Dockerfile-}
  echo "Tag: ${tag}"
  docker_tag="wallies/python-cuda:${tag}"

  (
     set -x
     docker build -t "$docker_tag" -f "$file" .
     echo "Successfully built $docker_tag"
  )

  (
     set -x
     docker push "$docker_tag"
     echo "Successfully built and pushed $docker_tag"
  )
done
