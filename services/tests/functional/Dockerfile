FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH /tests/functional

COPY entrypoint.sh .
COPY requirements.txt .

RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

COPY . /tests/functional
WORKDIR /tests/functional

RUN chmod a+x entrypoint.sh