#!/bin/bash
set -e
set -o pipefail

cd python-cuda
for dockerfile in Dockerfile-*; do
  image="${dockerfile%Dockerfile-*}"
  base="${image%%/*}"
  suite="${image##*/}"
  build_dir=python-cuda
  echo "image: ${image}"
  echo "base: ${base}"
  echo "suite: ${suite}"
  echo "directory: ${build_dir}"

  if [[ "$suite" =~ "Dockerfile" ]]; then
    suite="${suite#Dockerfile-}"
  fi
  
  docker_tag="wallies/${base}:${suite}"

  (
     set -x
     docker build -t "$docker_tag" -f "$dockerfile" .
     echo "Successfully built $docker_tag with context $build_dir"
  )

  (
     set -x
     docker push "$docker_tag"
     echo "Successfully built and pushed $docker_tag"
  )
done
