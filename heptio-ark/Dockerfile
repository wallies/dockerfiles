FROM alpine:3.7

ENV UID=991 \
    GID=991 \
    HEPTIO_ARK_VERSION=0.6.0

RUN apk add --update --no-cache tar curl su-exec tini && \
    curl -sLo /tmp/ark.tar.gz "https://github.com/heptio/ark/releases/download/v${HEPTIO_ARK_VERSION}/ark-v${HEPTIO_ARK_VERSION}-linux-amd64.tar.gz" && \
    tar -xvf /tmp/ark.tar.gz -C /usr/local/bin/ && \
    rm /tmp/ark.tar.gz /var/cache/apk/* && \
    apk del curl tar

RUN addgroup -g "${GID}" ark && \
    adduser -D -u "${UID}" -G ark ark

RUN chmod +x /usr/local/bin/ark && \
    chown -R ${UID}:${GID} /usr/local/bin/ark

USER ark

ENTRYPOINT ["/sbin/tini", "--"]
CMD ["/usr/local/bin/ark"]