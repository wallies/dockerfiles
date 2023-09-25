FROM alpine:3.10@sha256:451eee8bedcb2f029756dc3e9d73bab0e7943c1ac55cff3a4861c52a0fdd3e98

LABEL maintainer cam.parry@gmail.com

ENV SQL_LINT_VERSION=0.0.11

RUN apk add --update --no-cache curl && \
    curl -sLo /usr/local/bin/sql-lint "https://github.com/joereynolds/sql-lint/releases/download/v${SQL_LINT_VERSION}/sql-lint-linux" && \
    chmod +x /usr/local/bin/sql-lint && \
    apk del curl

WORKDIR /src