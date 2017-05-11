FROM python:3.6.0-alpine

RUN apk --update add --no-cache gcc build-base libxslt-dev libxml2-dev \
  && pip3 install mypy-lang mypy pylint lxml

RUN mkdir /src
WORKDIR /src

ENTRYPOINT ["mypy"]