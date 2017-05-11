FROM alpine:edge
MAINTAINER Wallies

ENV UID=991 \
    GID=991 \
    LDAP_SERVER_NAME='example.com' \
    LDAP_SERVER_PORT=389 \
    LDAP_SERVER_DN='dc=corp,dc=com'

ARG NGINX_VERSION=1.11.13
ARG GPG_NGINX="B0F4 2533 73F8 F6F5 10D4  2178 520A 9993 A1C0 52F8"
ARG BUILD_CORES

ARG NGINX_MODULES=" \
    --with-http_ssl_module \
    --with-http_v2_module \
    --with-http_gzip_static_module \
    --with-http_stub_status_module \
    --with-file-aio \
    --with-threads \
    --with-pcre-jit \
    --with-debug \
    --without-http_scgi_module \
    --without-http_uwsgi_module \
    --without-http_autoindex_module \
    --without-http_map_module \
    --without-http_split_clients_module \
    --without-http_memcached_module \
    --without-http_empty_gif_module"

ARG NGINX_3RD_PARTY_MODULES=" \
    --add-module=/tmp/headers-more-nginx-module \
    --add-module=/tmp/ngx_brotli" \
    --add-module=/tmp/nginx-auth-ldap"

RUN echo "@commuedge https://nl.alpinelinux.org/alpine/edge/community" >> /etc/apk/repositories \
 && NB_CORES=${BUILD_CORES-$(getconf _NPROCESSORS_CONF)} \
 && BUILD_DEPS=" \
    build-base \
    linux-headers \
    ca-certificates \
    automake \
    autoconf \
    git \
    tar \
    libtool \
    pcre-dev \
    zlib-dev \
    libressl-dev \
    openldap-dev \
    binutils \
    gnupg \
    cmake \
    curl \
    go" \
 && apk -U upgrade && apk add \
    ${BUILD_DEPS} \
    pcre \
    zlib \
    libgcc \
    libressl \
    openldap \
    libstdc++ \
    su-exec \
    bind-tools \
    libcap \
    tini@commuedge \
 && cd /tmp && git clone https://github.com/bagder/libbrotli --depth=1 \
 && cd libbrotli && ./autogen.sh && ./configure && make -j ${NB_CORES} && make install \
 && cd /tmp && git clone https://github.com/kvspb/nginx-auth-ldap.git --depth=1 \
 && git clone https://boringssl.googlesource.com/boringssl --depth=1 \
 && git clone https://github.com/openresty/headers-more-nginx-module --depth=1 \
 && curl -sLo /usr/local/bin/ep https://github.com/kreuzwerker/envplate/releases/download/v0.0.8/ep-linux \
 && chmod +x /usr/local/bin/ep \
 && cd boringssl \
 && sed -i 's@out \([>=]\) TLS1_2_VERSION@out \1 TLS1_3_VERSION@' ssl/ssl_lib.c \
 && sed -i 's@ssl->version[ ]*=[ ]*TLS1_2_VERSION@ssl->version = TLS1_3_VERSION@' ssl/s3_lib.c \
 && sed -i 's@(SSL3_VERSION, TLS1_2_VERSION@(SSL3_VERSION, TLS1_3_VERSION@' ssl/ssl_test.cc \
 && sed -i 's@\$shaext[ ]*=[ ]*0;@\$shaext = 1;@' crypto/*/asm/*.pl \
 && sed -i 's@\$avx[ ]*=[ ]*[0|1];@\$avx = 2;@' crypto/*/asm/*.pl \
 && sed -i 's@\$addx[ ]*=[ ]*0;@\$addx = 1;@' crypto/*/asm/*.pl \
 && mkdir build && cd build && cmake -DCMAKE_BUILD_TYPE=Release .. \
 && make -j ${NB_CORES} && cd .. \
 && mkdir -p .openssl/lib/ && cd .openssl && ln -s ../include && cd .. \
 && cp build/crypto/libcrypto.a build/ssl/libssl.a .openssl/lib && cd /tmp \
 && NGINX_TARBALL="nginx-${NGINX_VERSION}.tar.gz" \
 && wget -q https://nginx.org/download/${NGINX_TARBALL} \
 && echo "Verifying ${NGINX_TARBALL} using GPG..." \
 && wget -q https://nginx.org/download/${NGINX_TARBALL}.asc \
 && wget -q https://nginx.org/keys/mdounin.key \
 && gpg --import mdounin.key \
 && FINGERPRINT="$(LANG=C gpg --verify ${NGINX_TARBALL}.asc ${NGINX_TARBALL} 2>&1 \
  | sed -n "s#Primary key fingerprint: \(.*\)#\1#p")" \
 && if [ -z "${FINGERPRINT}" ]; then echo "Warning! Invalid GPG signature!" && exit 1; fi \
 && if [ "${FINGERPRINT}" != "${GPG_NGINX}" ]; then echo "Warning! Wrong GPG fingerprint!" && exit 1; fi \
 && echo "All seems good, now unpacking ${NGINX_TARBALL}..." \
 && tar xzf ${NGINX_TARBALL} && cd nginx-${NGINX_VERSION} \
 && wget -q https://raw.githubusercontent.com/cujanovic/nginx-dynamic-tls-records-patch/master/nginx__dynamic_tls_records_1.11.5%2B.patch -O dynamic_records.patch \
 && patch -p1 < dynamic_records.patch \
 && ./configure \
    --prefix=/etc/nginx \
    --sbin-path=/usr/sbin/nginx \
    --with-cc-opt="-O3 -fPIE -fstack-protector-strong -Wformat -Werror=format-security -Wno-deprecated-declarations -I ../boringssl/.openssl/include/" \" \
    --http-log-path=/var/log/nginx/access.log \
    --error-log-path=/var/log/nginx/error.log \
    ${NGINX_MODULES} \
    ${NGINX_3RD_PARTY_MODULES} \
    
 && make -j ${NB_CORES} && make install && make clean \
 && strip -s /usr/sbin/nginx \
 && apk del ${BUILD_DEPS} \
 && rm -rf /tmp/* /var/cache/apk/* /root/.gnupg

COPY nginx.conf /etc/nginx/conf/nginx.conf
COPY run.sh /usr/local/bin/run.sh
COPY ssl_params /etc/nginx/conf/ssl_params
COPY headers_params /etc/nginx/conf/headers_params
COPY proxy_params /etc/nginx/conf/proxy_params

RUN chmod +x /usr/local/bin/* \
    && setcap 'cap_net_bind_service=+ep' /usr/sbin/nginx

EXPOSE 8000 4430

VOLUME /sites-enabled /www /conf.d /certs /var/log/nginx

LABEL description="nginx built from source with ldap" \
      openssl="BoringSSL" \
      nginx="nginx ${NGINX_VERSION}"

CMD ["run.sh"]