FROM python:3.9-slim
WORKDIR /app
COPY . /app
RUN apt-get update && apt-get install -y     python3-pip     && pip install flask gunicorn redis
CMD ["gunicorn", "--bind", "0.0.0.0:80", "app:app"]
