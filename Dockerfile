FROM python:3.11

WORKDIR /app

COPY . /app

COPY data /app/data

RUN pip install -r requirements.txt

CMD [ "python", "./server.py" ]
