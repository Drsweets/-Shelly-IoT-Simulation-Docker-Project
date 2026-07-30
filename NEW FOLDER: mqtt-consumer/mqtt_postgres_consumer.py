import paho.mqtt.client as mqtt
import json
import psycopg2
import os
import time

# Load Environment Variables
MQTT_BROKER = os.getenv("MQTT_BROKER")
MQTT_TOPIC = os.getenv("MQTT_TOPIC")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

# Database Connection Helper
def create_db_connection():
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        return conn
    except Exception as e:
        print(f"⚠️ Database connection error: {e}")
        return None

# Initialize DB Table if not exists
def init_table():
    conn = create_db_connection()
    if not conn:
        return
    cur = conn.cursor()
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS shelly_metrics (
        id BIGSERIAL PRIMARY KEY,
        timestamp BIGINT NOT NULL,
        temp_c NUMERIC(5,2),
        power_watts NUMERIC(6,2),
        total_energy_kwh NUMERIC(6,3),
        online BOOLEAN
    );
    CREATE INDEX IF NOT EXISTS idx_shelly_ts ON shelly_metrics(timestamp);
    """
    cur.execute(create_table_sql)
    conn.commit()
    cur.close()
    conn.close()
    print("✅ Database table initialized or already exists")

# MQTT Message Handler
def on_message(client, userdata, message):
    try:
        payload = json.loads(message.payload.decode())
        conn = create_db_connection()
        if not conn:
            return
        cur = conn.cursor()
        insert_sql = """
        INSERT INTO shelly_metrics (timestamp, temp_c, power_watts, total_energy_kwh, online)
        VALUES (%s, %s, %s, %s, %s);
        """
        cur.execute(insert_sql, (
            payload["timestamp"],
            payload["temp_c"],
            payload["power_watts"],
            payload["total_energy_kwh"],
            payload["online"]
        ))
        conn.commit()
        cur.close()
        conn.close()
        print(f"💾 Saved metrics to DB: {payload}")
    except Exception as err:
        print(f"❌ Failed to process message: {err}")

def on_connect(client, userdata, flags, rc):
    print(f"✅ Consumer connected to MQTT broker, code: {rc}")
    client.subscribe(MQTT_TOPIC)
    print(f"📥 Subscribed to topic: {MQTT_TOPIC}")

# Main program flow
if __name__ == "__main__":
    # Wait for Postgres fully boot
    time.sleep(10)
    init_table()

    mqtt_client = mqtt.Client(client_id="shelly-mqtt-consumer")
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message

    mqtt_client.connect(MQTT_BROKER, 1883, 60)
    mqtt_client.loop_forever()
