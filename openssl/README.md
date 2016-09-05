# openssl
Debian based image with openssl for ssl certificate generation.

[Docker Image](https://hub.docker.com/r/wallies/openssl/)

[Image Layers](https://img.shields.io/imagelayers/image-size/wallies/openssl/latest.svg)

## Build openssl image

    docker build -t wallies/openssl --build-arg OPENSSL_VERSION=1.1.0 .

## Create a certificate

    docker run --rm -it --name openssl \
      -v $(pwd):/certs \
      wallies/openssl \
      openssl ecparam -list_curves
 
    docker run --rm -it --name openssl \
      -v $(pwd)/certs:/certs \
      wallies/openssl \
      openssl ecparam -out /certs/ec_key.pem \
      -name secp521r1 -noout -genkey

    docker run --rm -it --name openssl \
      -v $(pwd)/certs:/certs \
      -e ALT_NAME="DNS:xip.io,DNS:127.0.0.1.xip.io" \
      wallies/openssl \
      openssl req -new -key /certs/ec_key.pem \
      -sha256 -nodes -outform pem -reqexts SAN \
      -subj "/C=UK/ST=London/L=London/O=xip/OU=IT/CN=xip.io" \
      -out /certs/ecc.csr

## Result of the run

    ec_key.pem
    ecc.csr
    
