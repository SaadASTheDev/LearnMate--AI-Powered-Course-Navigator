# File: backend/monitoring.py

from flask import Flask, request
from prometheus_client import Counter, Histogram, generate_latest

app = Flask(__name__)

# Define Prometheus metrics
REQUEST_COUNT = Counter('recommendation_requests_total', 'Total number of recommendation requests', ['endpoint'])
SUCCESS_COUNT = Counter('successful_recommendations_total', 'Total number of successful recommendations', ['endpoint'])
REQUEST_LATENCY = Histogram('request_latency_seconds', 'Latency of HTTP requests in seconds', ['endpoint'])

# Example route with monitoring
@app.route('/api/recommend', methods=['GET'])
def recommend():
    endpoint = '/api/recommend'
    REQUEST_COUNT.labels(endpoint=endpoint).inc()
    with REQUEST_LATENCY.labels(endpoint=endpoint).time():
        try:
            # Simulate recommendation logic here
            # (Replace with actual recommendation code)
            SUCCESS_COUNT.labels(endpoint=endpoint).inc()
            return {"message": "Recommendation made successfully"}, 200
        except Exception as e:
            print(f"Error generating recommendation: {e}")
            return {"error": "Failed to generate recommendation"}, 500

# Metrics endpoint for Prometheus to scrape
@app.route('/metrics', methods=['GET'])
def metrics():
    return generate_latest(), 200

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5005)