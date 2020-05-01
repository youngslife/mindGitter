FROM python:3.8

WORKDIR /app

COPY requirements.txt /tmp/requirements.txt

RUN pip install -r /tmp/requirements.txt

COPY . /app

RUN chmod 755 start

ENTRYPOINT ["/app/start"]