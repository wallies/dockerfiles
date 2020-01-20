FROM alpine:3.10

LABEL maintainer cam.parry@gmail.com

LABEL Vendor="Wallies" \
      Name=lint-validator \
      JSON_LINT_VERSION=1.6.3 \
      SWAGGER_CLI_VERSION=2.3.3

RUN apk add --update nodejs nodejs-npm && \
    rm /var/cache/apk/*

RUN npm install -g \
	jsonlint \
	jsondiffpatch \
	prettyjson \
	json-minify \
	yaml-lint \
	swagger-cli


WORKDIR /src