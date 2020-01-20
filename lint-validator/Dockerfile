FROM alpine:3.10

LABEL maintainer cam.parry@gmail.com

LABEL Vendor="Wallies" \
      Name=lint-validator \
      JSON_LINT_VERSION=1.6.3 \
      SWAGGER_CLI_VERSION=2.3.5

ENV UID=1001 \
    GID=1002

RUN addgroup -g ${GID} validator && \
    adduser -D -u ${UID} -G validator validator

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

USER validator

CMD ["swagger-cli", "--version"]