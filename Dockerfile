FROM python:3.8-slim-buster
ENV PYTHONUNBUFFERED=1
WORKDIR /challenge
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .