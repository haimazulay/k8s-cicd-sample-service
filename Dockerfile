# test L1 workflow trigger
FROM python:3.12-slim

WORKDIR /app
COPY . /app

CMD ["python", "-c", "print('Hello from sample-service')"]
