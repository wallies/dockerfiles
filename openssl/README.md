# openssl
Debian based image with openssl for ssl certificate generation.

[![](https://images.microbadger.com/badges/version/wallies/openssl.svg)](http://microbadger.com/images/wallies/openssl "Get your own version badge on microbadger.com")

[![](https://images.microbadger.com/badges/image/wallies/openssl.svg)](http://microbadger.com/images/wallies/openssl "Get your own image badge on microbadger.com")

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
    
