FROM alpine:3.4

RUN apk --update add bash docker python \
  && rm -rf /var/cache/apk/*

COPY ./docker-gc /docker-gc

VOLUME /var/lib/docker-gc

CMD ["/docker-gc"]
