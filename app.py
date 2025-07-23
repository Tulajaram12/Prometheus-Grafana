from flask import Flask, request, Response
import time
import random
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
import logging

app = Flask(__name__)

# --- Metrics definitions ---

# Track total HTTP requests
http_requests_total = Counter(
    'http_requests_total', 'Total HTTP Requests',
    ['method', 'endpoint', 'http_status']
)

# Track HTTP request latency
http_request_latency = Histogram(
    'http_request_latency_seconds', 'Latency of HTTP requests',
    ['method', 'endpoint']
)

# Track HTTP errors (status 4xx and 5xx)
http_errors_total = Counter(
    'http_errors_total', 'Total HTTP Error Responses',
    ['method', 'endpoint', 'http_status']
)

# --- Middleware to collect metrics ---
@app.before_request
def start_timer():
    request.start_time = time.time()

@app.after_request
def record_metrics(response):
    latency = time.time() - request.start_time
    method = request.method
    endpoint = request.path
    status = response.status_code

    http_requests_total.labels(method, endpoint, status).inc()
    http_request_latency.labels(method, endpoint).observe(latency)

    if 400 <= status < 600:
        http_errors_total.labels(method, endpoint, status).inc()

    return response

# --- Endpoints ---

@app.route('/')
def home():
    app.logger.info("Home page accessed")
    return 'Hello from Flask!', 200

@app.route('/error')
def error():
    return 'This is an error!', 500

@app.route('/random')
def random_response():
    if random.random() < 0.3:
        return 'Oops, something went wrong', 500
    return 'All good!', 200

# --- Expose Prometheus metrics ---
@app.route('/metrics')
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

# --- Run the app ---
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)

