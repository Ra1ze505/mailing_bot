FROM python:3.11

WORKDIR /usr/app/

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV POETRY_VERSION=1.5.1

# RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | POETRY_HOME=/opt/poetry python && \
#     cd /usr/local/bin && \
#     ln -s /opt/poetry/bin/poetry && \
#     poetry config virtualenvs.create false

RUN pip install "poetry==$POETRY_VERSION"



RUN apt-get -y update
RUN apt-get -y upgrade

COPY ./poetry.lock ./pyproject.toml /usr/app/

# RUN poetry install

# Project initialization:
RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi

COPY . /usr/app/

#RUN ls
# CMD ["python3", "$EXECUTE_PATH"]
