FROM python:3.10-alpine

WORKDIR /app
COPY requirements.txt .

RUN apk add --no-cache \
    build-base \ 
    gcc \
    musl-dev \
    postgresql-dev

RUN pip install -r requirements.txt

EXPOSE 5000