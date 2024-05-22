FROM python:3.10

WORKDIR /tests

COPY ./tests/functional/requirements.txt .
RUN pip3 install --upgrade pip
RUN pip3 install --no-cache-dir -r requirements.txt

COPY ./tests .