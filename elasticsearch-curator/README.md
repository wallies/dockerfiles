## About:

* [Elasticsearch Curator](https://github.com/elasticsearch/curator)

## Usage:

```ENTRYPOINT``` is set to ```/usr/bin/curator``` so you can just do something like

```
docker run --rm wallies/elasticsearch-curator:3.5.1 --host $IP show --show-indices
```
