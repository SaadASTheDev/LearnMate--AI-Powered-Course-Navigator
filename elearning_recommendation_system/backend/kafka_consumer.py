# File: backend/kafka_consumer.py

from kafka import KafkaConsumer
import json
import psycopg2
import os

# Set up database connection parameters
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_NAME = os.getenv('DB_NAME', 'elearn')
DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'secret')

# Function to get a connection to the database
def get_db_connection():
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        return conn
    except psycopg2.DatabaseError as e:
        print(f"Database connection error: {e}")
        return None

# Configure Kafka Consumer
consumer = KafkaConsumer(
    'user_interactions',
    bootstrap_servers=['localhost:9092'],
    value_deserializer=lambda v: json.loads(v.decode('utf-8'))
)

def process_interaction(event):
    user_id = event.get('user_id')
    course_id = event.get('course_id')
    interaction_type = event.get('interaction_type')
    timestamp = event.get('timestamp')

    if not user_id or not course_id or not interaction_type:
        print("Invalid event data, skipping...")
        return

    conn = get_db_connection()
    if conn is None:
        print("Failed to connect to the database, skipping event...")
        return

    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO UserCourseInteractions (user_id, course_id, interaction_type, created_at)
            VALUES (%s, %s, %s, to_timestamp(%s))
            """,
            (user_id, course_id, interaction_type, timestamp)
        )
        conn.commit()
        cursor.close()
        print(f"Processed event: {event}")
    except Exception as e:
        print(f"Error inserting interaction: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    print("Kafka Consumer is listening for user interactions...")
    for message in consumer:
        event = message.value
        process_interaction(event)