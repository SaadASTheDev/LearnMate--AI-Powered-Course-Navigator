# File: backend/kafka_producer.py

from kafka import KafkaProducer
import json
import time

# Configure Kafka Producer
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def send_interaction_event(user_id, course_id, interaction_type):
    # Create the event message
    event = {
        'user_id': user_id,
        'course_id': course_id,
        'interaction_type': interaction_type,
        'timestamp': time.time()
    }
    
    # Send the event to the Kafka topic 'user_interactions'
    producer.send('user_interactions', value=event)
    print(f"Sent event: {event}")

if __name__ == "__main__":
    # Example usage: Sending a test interaction
    user_id = 1
    course_id = 101
    interaction_type = 'enrollment'
    
    send_interaction_event(user_id, course_id, interaction_type)
    
    # Allow time for the message to be sent before closing
    producer.flush()
    producer.close()