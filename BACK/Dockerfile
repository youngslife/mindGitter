FROM python:3.8

COPY . /app
WORKDIR /app
EXPOSE 8000

RUN pip install --upgrade pip && pip install -r requirements.txt

RUN chmod 755 /app/start
ENTRYPOINT [ "/app/start" ]