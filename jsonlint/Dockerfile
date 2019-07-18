FROM alpine:3.10

LABEL maintainer cam.parry@gmail.com

LABEL Vendor="Wallies" \
      Name=jsonlint \
      Version=1.6.3

RUN apk add --update nodejs nodejs-npm && \
    rm /var/cache/apk/*

RUN npm install -g jsonlint jsondiffpatch prettyjson json-minify

WORKDIR /src