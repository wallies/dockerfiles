FROM alpine:3.10

LABEL maintainer cam.parry@gmail.com

ENV SQL_LINT_VERSION=0.0.11

RUN apk add --update --no-cache curl && \
    curl -sLo /usr/local/bin/sql-lint "https://github.com/joereynolds/sql-lint/releases/download/v${SQL_LINT_VERSION}/sql-lint-linux" && \
    chmod +x /usr/local/bin/sql-lint && \
    apk del curl

WORKDIR /src