# File: backend/ab_testing.py

from flask import Flask, request, jsonify
import random
import pickle

app = Flask(__name__)

# Load two versions of the recommendation model
with open('ml_models/model_a.pkl', 'rb') as file:
    model_a = pickle.load(file)

with open('ml_models/model_b.pkl', 'rb') as file:
    model_b = pickle.load(file)

# Endpoint to provide recommendations using A/B testing
@app.route('/api/ab_recommend', methods=['GET'])
def ab_recommend():
    user_id = request.args.get('userId', type=int)
    if not user_id:
        return jsonify({"error": "User ID is required"}), 400

    # Randomly assign the user to either model A or model B
    assigned_model = random.choice(['A', 'B'])
    try:
        if assigned_model == 'A':
            recommendations = model_a.recommend(user_id, [])
        else:
            recommendations = model_b.recommend(user_id, [])

        return jsonify({"model": assigned_model, "recommendations": recommendations})
    except Exception as e:
        print(f"Error generating recommendations: {e}")
        return jsonify({"error": "Failed to generate recommendations"}), 500

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5004)