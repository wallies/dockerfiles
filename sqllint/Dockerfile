FROM alpine:3.10

LABEL maintainer cam.parry@gmail.com

ENV UID=991 \
    GID=991 \
    SQL_LINT_VERSION=0.0.11

RUN apk add --update --no-cache curl su-exec tini && \
    curl -sLo /usr/local/bin/sql-lint "https://github.com//joereynolds/sql-lint/releases/download/v${HEPTIO_VELERO_VERSION}/sql-lint-linux" && \
    apk del curl

RUN addgroup -g "${GID}" sqllint && \
    adduser -D -u "${UID}" -G sqllint sqllint

RUN chmod +x /usr/local/bin/sql-lint && \
    chown -R ${UID}:${GID} /usr/local/bin/sql-lint

USER sqllint

ENTRYPOINT ["/sbin/tini", "--"]
CMD ["/usr/local/bin/sql-lint"]
