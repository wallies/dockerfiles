FROM python:3.9-alpine3.12@sha256:7f73901e568630443fc50e358b76603492e89c9bf330caf689e856a018f135f0

ENV SOURCE=/source \
    OUTPUT=/output \
    UID=1001 \
    GID=1002

# ensure local python is preferred over distribution python
ENV PATH /usr/local/bin:$PATH

# http://bugs.python.org/issue19846
# > At the moment, setting "LANG=C" on a Linux system *fundamentally breaks Python 3*, and that's not OK.
ENV LANG C.UTF-8

COPY ./dependencies/alpine /var/run/runtime-deps-pkgs
COPY ./dependencies/pip /var/run/runtime-deps-pip

# Create a servicelayer user and group first so the IDs get set the same way,
# even as the rest of this may change over time.
RUN addgroup -g ${GID} pytester && \
    adduser -D -u ${UID} -G pytester pytester


RUN apk --update-cache add hub --repository http://dl-cdn.alpinelinux.org/alpine/edge/testing \
    && apk add --update-cache $(cat /var/run/runtime-deps-pkgs) \
    && wget https://github.com/stedolan/jq/releases/latest/download/jq-linux64 -O /usr/local/bin/jq \
    && pip3 install -U pip setuptools requests requests-toolbelt \
    && pip3 install $(cat /var/run/runtime-deps-pip)

RUN mkdir -p $SOURCE $OUTPUT /src/tasks && \
    chown -R pytester:pytester $SOURCE $OUTPUT /src /tmp \
    /usr/local/lib/python3.9 /usr/local/bin /usr/bin/ssh && \
    chmod +x /usr/local/bin/jq 

WORKDIR $SOURCE

USER pytester

CMD ["python", "-V"]
