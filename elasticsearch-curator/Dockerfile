# Elasticsearch Curator

FROM python:2.7-alpine

RUN pip install "elasticsearch-curator<4.0.0"

USER nobody

ENTRYPOINT ["/usr/bin/curator"]

CMD ["--help"]
