FROM python:3.9

ENV PYTHONUNBUFFERED 1

WORKDIR /app

#Install Poetry
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

# Install ping utility
RUN apt-get update

RUN apt-get install -y iputils-ping

COPY pyproject.toml poetry.lock* /app/

# Install dev dependencies to run tests
ARG INSTALL_DEV=true
RUN bash -c "if [ $INSTALL_DEV == 'true' ] ; then poetry install --no-root ; else poetry install --no-root --no-dev ; fi"

COPY . .

##CMD [ "flask", "run", "--host=0.0.0.0"]
#
ENTRYPOINT ["./app/script/entrypoint"]












#FROM python:3.8-slim as base
#
#FROM base as builder
#
#RUN mkdir /install
#WORKDIR /install
#
#COPY requirements.txt /requirements.txt
#
#RUN pip install --prefix=/install -r /requirements.txt
#
#FROM base
#
#COPY --from=builder /install /usr/local
#
#COPY . /app
#
#WORKDIR /app
#CMD "./gunicorn_starter.sh"
