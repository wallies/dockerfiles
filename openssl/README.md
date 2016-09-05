# openssl
Debian based image with openssl for ssl certificate generation.

## Build openssl image

    docker build -t wallies/openssl --build-arg OPENSSL_VERSION=1.1.0 .

## Create a certificate

    docker run --rm -it --name openssl \
      -e  KEY_NAME=mykey \
      -e  KEY_SIZE=4096 \
      -e  COUNTRY=UK \
      -e  STATE="Greater London"
      -e  LOCATION=London \
      -e  ORGANISATION=example \
      -e  DAYS=365 \
      -v $(pwd):/certs \
      wallies/openssl

## Result of the run

    -rw-r--r-- 1 root root 1212 10 mars  14:31 mykey.crt
    -rw-r--r-- 1 root root 1009 10 mars  14:31 mykey.csr
    -rw-r--r-- 1 root root 1675 10 mars  14:31 mykey.key
