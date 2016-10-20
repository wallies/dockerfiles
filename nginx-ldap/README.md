# nginx-ldap
alpine based nginx with ldap auth support.

[![](https://images.microbadger.com/badges/version/wallies/nginx-ldap.svg)](https://microbadger.com/images/wallies/nginx-ldap "Get your own version badge on microbadger.com")

[![](https://images.microbadger.com/badges/version/wallies/nginx-ldap.svg)](https://microbadger.com/images/wallies/nginx-ldap "Get your own version badge on microbadger.com")

## Build image

    docker build -t wallies/nginx-ldap .

## Run

    docker run --name nginx \
    --rm -it \
    --privileged=true \
    -p 443:4430 \
    -p 80:8000
    -e LDAP_SERVER_NAME=ldap.example.com \ 
    -e LDAP_SERVER_DN=dc=example,dc=com \ 
    --add-host=ldap.example.com:127.0.0.1 \
    -v /etc/nginx/sites-enabled/vhost.conf:/sites-enabled/vhost.conf \
    wallies/nginx-ldap:latest

You will notice above I am using add-host option, this is to mitigate being on the bridge network and the host not being able to see the ldap host, which is not managed by docker.
