# docker-gc

## This is a fork from the amazing work from the team at Spotify - https://github.com/spotify/docker-gc

* [Usage](#usage)
  * [Excluding Images From Garbage Collection](#excluding-images-from-garbage-collection)
  * [Excluding Containers From Garbage Collection](#excluding-containers-from-garbage-collection)
  * [Running as a Docker Image](#running-as-a-docker-image)
    * [Build the Docker Image](#build-the-docker-image)
    * [Running as a Docker Container](#running-as-a-docker-container)

A simple Docker container and image garbage collection script.

* Containers that exited more than an hour ago are removed.
* Images that don't belong to any remaining container after that are removed.

Although docker normally prevents removal of images that are in use by
containers, we take extra care to not remove any image tags (e.g., ubuntu:14.04,
busybox, etc) that are in use by containers. A naive `docker rmi $(docker images
-q)` will leave images stripped of all tags, forcing docker to re-pull the
repositories when starting new containers even though the images themselves are
still on disk.


## Manual Usage

To use the script manually, run `docker-gc`. The system user under
which `docker-gc` runs needs to have read and write access to
the `$STATE_DIR` environment variable which defaults to `/var/lib/docker-gc`.


### Excluding Images From Garbage Collection

There can be images that are large that serve as a common base for
many application containers, and as such, make sense to pin to the
machine, as many derivative containers will use it.  This can save
time in pulling those kinds of images.  There may be other reasons to
exclude images from garbage collection.  To do so, create
`/etc/docker-gc-exclude`, or if you want the file to be read from
elsewhere, set the `EXCLUDE_FROM_GC` environment variable to its
location.  This file can contain image name patterns (in the `grep`
sense), one per line, such as `spotify/cassandra:latest` or it can
contain image ids (truncated to the length shown in `docker images`
which is 12.

An example image excludes file might contain:
```
spotify/cassandra:latest
redis:.*
9681260c3ad5
```

### Excluding Containers From Garbage Collection

There can also be containers (for example data only containers) which 
you would like to exclude from garbage collection. To do so, create 
`/etc/docker-gc-exclude-containers`, or if you want the file to be 
read from elsewhere, set the `EXCLUDE_CONTAINERS_FROM_GC` environment 
variable to its location. This file should container name patterns (in 
the `grep` sense), one per line, such as `mariadb-data`.

An example container excludes file might contain:
```
mariadb-data
drunk_goodall
```

### Forcing deletion of images that have multiple tags

By default, docker will not remove an image if it is tagged in multiple
repositories.
If you have a server running docker where this is the case, for example
in CI environments where dockers are being built, re-tagged, and pushed,
you can enable a force flag to override this default.

```
FORCE_IMAGE_REMOVAL=1 docker-gc
```

### Forcing deletion of containers

By default, if an error is encountered when cleaning up a container, Docker
will report the error back and leave it on disk.  This can sometimes lead to
containers accumulating.  If you run into this issue, you can force the removal
of the container by setting the environment variable below:

```
FORCE_CONTAINER_REMOVAL=1 docker-gc
```

### Excluding Recently Exited Containers and Images From Garbage Collection

By default, docker-gc will not remove a container if it exited less than 3600 seconds (1 hour) ago. In some cases you might need to change this setting (e.g. you need exited containers to stick around for debugging for several days). Set the `GRACE_PERIOD_SECONDS` variable to override this default.

```
GRACE_PERIOD_SECONDS=86400 docker-gc
```

This setting also prevents the removal of images that have been created less than `GRACE_PERIOD_SECONDS` seconds ago.

```
MINIMUM_IMAGES_TO_SAVE=2 docker-gc
```

This setting takes the images listed in the excluded file and only keeps the number of images specified.

### Dry run
By default, docker-gc will proceed with deletion of containers and images. To test your command-line options set the `DRY_RUN` variable to override this default.

```
DRY_RUN=1 docker-gc
```


## Running as a Docker Image

A Dockerfile is provided as an alternative to a local installation. By default
the container will start up, run a single garbage collection, and shut down.

The image is published as `wallies/docker-gc`.

#### Building the Docker Image
The image is currently built with Docker 1.12.0, but to build it against a newer
Docker version (to ensure that the API version of the command-line interface
matches with your Docker daemon), simply edit [the `ENV DOCKER_VERSION` line in
`Dockerfile`][dockerfile-ENV] prior to the build step below.


```sh
docker build -t wallies/docker-gc .
```

#### Running as a Docker Container

The docker-gc container requires access to the docker socket in order to
function, so you need to map it when running, e.g.:

```sh
$ docker run --rm -v /var/run/docker.sock:/var/run/docker.sock -v /etc:/etc walliesß/docker-gc
```

The `/etc` directory is also mapped so that it can read any exclude files
that you've created.
