# File: scripts/extract_interactions.py

import psycopg2
import csv
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

# Function to extract user-course interaction data and save it to a CSV file
def extract_interactions():
    conn = get_db_connection()
    if conn is None:
        print("Failed to connect to the database, exiting...")
        return

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT user_id, course_id, interaction_type, created_at FROM UserCourseInteractions")

        # Write the data to a CSV file
        output_file = 'data/user_course_interactions.csv'
        with open(output_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['user_id', 'course_id', 'interaction_type', 'created_at'])
            for row in cursor.fetchall():
                writer.writerow(row)

        print(f"Data successfully extracted to {output_file}")
    except Exception as e:
        print(f"Error extracting data: {e}")
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    extract_interactions()