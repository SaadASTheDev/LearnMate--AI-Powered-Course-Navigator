# Backend API for ML-powered Recommendation System using Flask

# Step 1: Install Flask
# Run the following command in your terminal to install Flask:
# pip install flask psycopg2-binary

# Step 2: Create Backend API
# File: backend/recommend.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
import pickle
import os

app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing for all routes

# Step 3: Set Up Database Connection
# PostgreSQL connection parameters
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_NAME = os.getenv('DB_NAME', 'elearn')
DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'secret')

# Establish connection to the PostgreSQL database
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

# Load trained recommendation model
model_file = 'ml_models/model.pkl'
try:
    with open(model_file, 'rb') as file:
        recommendation_model = pickle.load(file)
except FileNotFoundError:
    print(f"Model file not found: {model_file}")
    recommendation_model = None

# Step 4: Define API Endpoints

# Endpoint to get course recommendations for a user
@app.route('/get_recommendations', methods=['GET'])
def get_recommendations():
    user_id = request.args.get('userId', type=int)
    if not user_id:
        return jsonify({"error": "User ID is required"}), 400

    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Failed to connect to the database"}), 500

    try:
        # Get user-course interactions from the database
        cursor = conn.cursor()
        cursor.execute("SELECT course_id FROM UserCourseInteractions WHERE user_id = %s", (user_id,))
        interactions = cursor.fetchall()
        course_ids = [interaction[0] for interaction in interactions]
        cursor.close()

        # Use the recommendation model to get course recommendations
        if recommendation_model is None:
            return jsonify({"error": "Recommendation model is not available"}), 500

        recommended_courses = recommendation_model.recommend(user_id, course_ids)
        return jsonify(recommended_courses)
    except Exception as e:
        print(f"Error getting recommendations: {e}")
        return jsonify({"error": "Failed to get recommendations"}), 500
    finally:
        conn.close()

# Endpoint to update user-course interactions
@app.route('/update_interactions', methods=['POST'])
def update_interactions():
    data = request.get_json()
    user_id = data.get('userId')
    course_id = data.get('courseId')
    interaction_type = data.get('interactionType')

    if not user_id or not course_id or not interaction_type:
        return jsonify({"error": "User ID, Course ID, and Interaction Type are required"}), 400

    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Failed to connect to the database"}), 500

    try:
        # Insert new interaction into the database
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO UserCourseInteractions (user_id, course_id, interaction_type) VALUES (%s, %s, %s)",
            (user_id, course_id, interaction_type)
        )
        conn.commit()
        cursor.close()
        return jsonify({"message": "Interaction updated successfully"})
    except Exception as e:
        print(f"Error updating interaction: {e}")
        return jsonify({"error": "Failed to update interaction"}), 500
    finally:
        conn.close()

# Health check endpoint
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "OK"})

# Step 5: Run Flask Application
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

# Step 6: Connect Front-end and Back-end
# Use axios in the front-end to make GET requests to `/get_recommendations` and POST requests to `/update_interactions`.
