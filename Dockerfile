#Lightweight version of Python
FROM python:3.9-alpine3.13 
LABEL maintainer="pranjalsrivastava52@gmail.com"

#To avoid delays from the outputs to be printed from python
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
COPY ./scripts /scripts
COPY ./app /app

#Set the default path where the commands will be run from
WORKDIR /app
EXPOSE 8000

# Default env is set to non DEV (to be overidden in docker-compose.yml to run on local)
ARG DEV=false

# Running multiple commands from single RUN command to avoid multiple image layers. Using "&& \" can run multiple commands from different lines.
# 1) Create a venv 2) Upgrade pip 3) Install all dependencies from requirements.txt
# 4) Remove the tmp dir 5) Add a new user to the docker image (avoid using root user) 
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    apk add --update --no-cache postgresql-client jpeg-dev && \
    apk add --update --no-cache --virtual .tmp-build-deps \
        build-base postgresql-dev musl-dev zlib zlib-dev linux-headers && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    if [ $DEV = "true" ]; \
        then /py/bin/pip install -r /tmp/requirements.dev.txt ; \
    fi && \
    rm -rf /tmp && \
    apk del .tmp-build-deps && \
    adduser \
        --disabled-password \
        --no-create-home \
        django-user && \
    # Create the media nd static subfolders 
    # -p is passed to create all the subdirectories required 
    # for the path
    mkdir -p /vol/web/media && \
    mkdir -p /vol/web/static && \
    chown -R django-user:django-user /vol && \
    chmod -R 755 /vol && \
    chmod -R +x /scripts

#Adds Python bin and scripts to path of the docker image
ENV PATH="/scripts:/py/bin:$PATH"

#Switch to django-user
USER django-user

CMD ["run.sh"]