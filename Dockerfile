FROM python:3.4
RUN apt-get update -y
RUN apt-get install -y python-pip build-essential
COPY ./app /app
WORKDIR /app
RUN pip install --no-cache-dir -r requirements.txt
ENV FLASK_APP=server.py
ENV FLASK_ENV=development