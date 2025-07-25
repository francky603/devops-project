FROM python:3.9-slim
WORKDIR /app
COPY . /app
COPY /home/franky/voting-app/server.crt /app/server.crt
COPY /home/franky/voting-app/server.key /app/server.key
RUN pip install --no-cache-dir flask redis gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:443", "--certfile=/app/server.crt", "--keyfile=/app/server.key", "app:app"]
