FROM python:3.7-alpine@sha256:9d9b05fc8acdc85a9fc0da1da11a8e90f76b88bd36fabb8f57c4c7ef027fbcc9

RUN apk --update add --no-cache gcc build-base libxslt-dev libxml2-dev \
  && pip3 install mypy-lang mypy pylint lxml

RUN mkdir /src
WORKDIR /src

ENTRYPOINT ["mypy"]