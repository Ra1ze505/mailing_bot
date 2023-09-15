FROM python:3.11

WORKDIR /usr/app/

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV POETRY_VERSION=1.5.1

RUN pip install "poetry==$POETRY_VERSION"

RUN apt-get -y update
RUN apt-get -y upgrade

COPY ./poetry.lock ./pyproject.toml /usr/app/

# Project initialization:
RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi

COPY . /usr/app/
