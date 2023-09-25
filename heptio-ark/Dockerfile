FROM alpine:3.10@sha256:451eee8bedcb2f029756dc3e9d73bab0e7943c1ac55cff3a4861c52a0fdd3e98

ENV UID=991 \
    GID=991 \
    HEPTIO_VELERO_VERSION=1.0.0

RUN apk add --update --no-cache tar curl su-exec tini && \
    curl -sLo /tmp/velero.tar.gz "https://github.com/heptio/velero/releases/download/v${HEPTIO_VELERO_VERSION}/velero-v${HEPTIO_VELERO_VERSION}-linux-amd64.tar.gz" && \
    tar -xvf /tmp/velero.tar.gz --strip 1 -C /usr/local/bin/ && \
    rm /tmp/velero.tar.gz && \
    apk del curl tar

RUN addgroup -g "${GID}" velero && \
    adduser -D -u "${UID}" -G velero velero

RUN chmod +x /usr/local/bin/velero && \
    chown -R ${UID}:${GID} /usr/local/bin/velero

USER velero

ENTRYPOINT ["/sbin/tini", "--"]
CMD ["/usr/local/bin/velero"]
