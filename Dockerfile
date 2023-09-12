# app/Dockerfile

FROM python:3.9-slim

WORKDIR /usr/src/app

COPY ./app/requirements.txt /usr/src/app/requirements.txt

RUN apt-get update && apt-get install -y \
    build-essential \
    wget \
    libaio1 \
    unzip

RUN cd /opt && wget https://download.oracle.com/otn_software/linux/instantclient/1920000/instantclient-basic-linux.x64-19.20.0.0.0dbru.zip

RUN cd /opt && unzip instantclient-basic-linux.x64-19.20.0.0.0dbru.zip

RUN cd /opt && sh -c "echo /opt/instantclient_19_20 > /etc/ld.so.conf.d/oracle-instantclient.conf"

RUN ldconfig

RUN pip install --upgrade pip setuptools wheel \
    && pip install -r requirements.txt \
    && rm -rf /root/.cache/pip
