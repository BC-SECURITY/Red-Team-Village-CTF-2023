FROM python:3.8-slim-buster

WORKDIR /root

COPY . /root

COPY data /app/data

RUN pip install -r requirements.txt

EXPOSE 8045

CMD [ "python", "/root/server.py" ]
