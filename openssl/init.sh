#!/bin/sh
set -e

cat <<EOT >> /usr/local/ssl/openssl.cnf
[SAN]
subjectAltName=${ALT_NAME}
EOT

exec "$@"
