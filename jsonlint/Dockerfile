FROM alpine:3.10@sha256:451eee8bedcb2f029756dc3e9d73bab0e7943c1ac55cff3a4861c52a0fdd3e98

LABEL maintainer cam.parry@gmail.com

LABEL Vendor="Wallies" \
      Name=jsonlint \
      Version=1.6.3

RUN apk add --update nodejs nodejs-npm && \
    rm /var/cache/apk/*

RUN npm install -g jsonlint jsondiffpatch prettyjson json-minify

WORKDIR /src