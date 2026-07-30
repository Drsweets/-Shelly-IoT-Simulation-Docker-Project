FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir paho-mqtt psycopg2-binary
COPY mqtt_postgres_consumer.py .
CMD ["python", "mqtt_postgres_consumer.py"]
