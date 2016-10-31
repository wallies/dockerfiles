FROM alpine:3.4

ENV DOCKER_VERSION 1.11.2-r1

RUN apk --update add bash docker-${DOCKER-VERSION} python \
  && rm -rf /var/cache/apk/*

COPY ./docker-gc /docker-gc

VOLUME /var/lib/docker-gc

CMD ["/docker-gc"]
