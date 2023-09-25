FROM alpine:3.5@sha256:66952b313e51c3bd1987d7c4ddf5dba9bc0fb6e524eed2448fa660246b3e76ec

ARG NGINX_CONF_DIR=/etc/nginx
ARG PYPICLOUD_CONF_DIR=/etc/pypicloud
ARG PYPICLOUD_VERSION=0.5.3
ARG SUPERVISOR_CONF_DIR=/etc/supervisord
ARG TEMPLATES_DIR=/templates

ENV HTTP_PORT=$HTTP_PORT \
    NGINX_CONF=${NGINX_CONF_DIR}/nginx.conf \
    NGINX_CONF_TEMPLATE=${TEMPLATES_DIR}/nginx.conf.tmpl \
    PYPICLOUD_INI=${PYPICLOUD_CONF_DIR}/pypicloud.ini \
    PYPICLOUD_INI_TEMPLATE=${TEMPLATES_DIR}/pypicloud.ini.tmpl \
    PYPICLOUD_WORK_DIR=/var/lib/pypicloud \
    SUPERVISOR_CONF=${SUPERVISOR_CONF_DIR}/supervisord.conf \
    SUPERVISOR_CONF_TEMPLATE=${TEMPLATES_DIR}/supervisord.conf.tmpl

# Install packages
RUN apk add --no-cache --virtual runtime-deps bash ca-certificates cyrus-sasl gettext gzip libressl \
    nginx openldap py-crypto py-pip python supervisor uwsgi-python && \
    apk add --no-cache --virtual build-deps build-base cyrus-sasl-dev libressl-dev openldap-dev python2-dev && \
    pip install --upgrade pip && \
    pip install "pypicloud==${PYPICLOUD_VERSION}" requests pastescript redis \
    && apk del build-deps \
    && rm -f "${NGINX_CONF_DIR}/conf.d/default.conf" "${NGINX_CONF}"

# Setup runtime directories and entrypoint script.
RUN mkdir -p "${PYPICLOUD_WORK_DIR}/packages" "${TEMPLATES_DIR}" "${PYPICLOUD_CONF_DIR}" \
    "${SUPERVISOR_CONF_DIR}"

COPY assets/templates/* "${TEMPLATES_DIR}/"
COPY assets/pypicloud.ini "${PYPICLOUD_INI}"
COPY assets/entrypoint.sh /

RUN chmod +x /entrypoint.sh

VOLUME [ "${PYPICLOUD_WORK_DIR}" ]

EXPOSE 80

CMD ["/entrypoint.sh"]
