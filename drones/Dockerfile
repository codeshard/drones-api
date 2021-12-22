# syntax=docker/dockerfile:1
FROM python:3.9-slim
LABEL maintainer="Ozkar L. Garcell  <ozkar.garcell@gmail.com>"

ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100

#create app folder inside container
RUN mkdir /src
WORKDIR /src

# python dependencies
COPY requirements/base.txt /src/requirements.txt
RUN pip install -r requirements.txt
