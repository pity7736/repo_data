FROM python:3.8

ENV PYTHONUNBUFFERED=1
ENV CODE=/code

COPY requirements.txt .
RUN apt-get update && apt-get -y upgrade
RUN pip install -r requirements.txt

WORKDIR $CODE
