from flask import Flask, Response
import psutil
from prometheus_client import Gauge, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)

cpu_usage = Gauge("cpu_usage_percent", "CPU usage percent")
memory_usage = Gauge("memory_usage_percent", "Memory usage percent")

@app.route("/")
def home():
    return "Server Monitor Running"

@app.route("/metrics")
def metrics():
    cpu_usage.set(psutil.cpu_percent(interval=1))
    memory_usage.set(psutil.virtual_memory().percent)
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
