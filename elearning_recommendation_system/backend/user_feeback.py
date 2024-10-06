# File: backend/user_feedback.py

from flask import Flask, request, jsonify
from db import get_db_connection

app = Flask(__name__)

# Endpoint to collect user feedback
@app.route('/feedback', methods=['POST'])
def gather_feedback():
    data = request.get_json()
    user_id = data.get('userId')
    course_id = data.get('courseId')
    feedback = data.get('feedback')

    if not user_id or not course_id or not feedback:
        return jsonify({"error": "User ID, Course ID, and Feedback are required"}), 400

    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO UserFeedback (user_id, course_id, feedback, created_at)
            VALUES (%s, %s, %s, NOW())
            """,
            (user_id, course_id, feedback)
        )
        conn.commit()
        cursor.close()
        return jsonify({"message": "Feedback recorded successfully"}), 201
    except Exception as e:
        print(f"Error inserting feedback: {e}")
        return jsonify({"error": "Failed to record feedback"}), 500
    finally:
        conn.close()

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5003)