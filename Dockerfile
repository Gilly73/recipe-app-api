FROM python:3.9-alpine3.13
LABEL maintainer="sgilldocker"

# wanting to see output in console so asked for unbuffered output
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
COPY ./app /app
WORKDIR /app
EXPOSE 8000

# DEV default=false and then updated by docker-compose.yml file
ARG DEV=false 

# run as one command so docker doesn't create a layer for each command
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    #install the client package to connect to the database from alpine image
    apk add --update --no-cache postgresql-client && \
    # virtual dependancies for building the python packages to remove later on below
    apk add --update --no-cache --virtual .tmp-build-deps \
    #packages to install to build the other db dependancies in virtual env
        build-base postgresql-dev musl-dev && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    if [ $DEV = "true" ]; \
        then /py/bin/pip install -r /tmp/requirements.dev.txt ; \
    fi && \
    rm -rf /tmp && \
    # remove the virtual dependancies that were used to build the python packages above
    apk del .tmp-build-deps && \
    adduser \
        --disabled-password \
        --no-create-home \
        django-user

ENV PATH="/py/bin:$PATH"

USER django-user