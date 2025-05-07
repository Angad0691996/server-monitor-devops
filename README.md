# Server Monitor DevOps Setup

## Introduction

This project sets up a monitoring stack consisting of Prometheus, Grafana, and a Flask-based server monitor application using Docker Compose. The setup allows you to monitor server metrics and visualize them using Grafana.

---

## Prerequisites

Ensure the following are installed on your EC2 instance:

* Docker
* Docker Compose
* Git

---

## Project Structure

```
server-monitor-devops/
├── app/
│   └── run.py            # Flask application
├── docker-compose.yml    # Docker Compose configuration
├── prometheus/
│   └── prometheus.yml    # Prometheus configuration
├── grafana_data/         # Grafana data persistence (will be created)
├── requirements.txt      # Python dependencies
└── Jenkinsfile           # CI/CD pipeline configuration
```

---

## Setup and Configuration

1. **Clone the repository:**

```bash
cd /home/ubuntu
git clone https://github.com/Angad0691996/server-monitor-devops.git
cd server-monitor-devops
```

2. **Build the Flask application Docker image:**

```bash
docker build -t flask_app .
```

3. **Ensure the Prometheus configuration file is present:**

* Verify that `prometheus/prometheus.yml` is properly configured.

4. **Update `docker-compose.yml` if necessary.**

---

## Starting the Application

To start the monitoring stack, execute:

```bash
cd /home/ubuntu/server-monitor-devops
docker-compose up -d --build
```

* This will build and start the following containers:

  * `server-monitor`: Flask application (Port 5000)
  * `prometheus`: Prometheus server (Port 9090)
  * `grafana`: Grafana server (Port 3000)

---

## Accessing Prometheus and Grafana

* Prometheus: `http://<EC2_IP>:9090`
* Grafana: `http://<EC2_IP>:3000`

  * Default username: `admin`
  * Default password: `admin`

---

## Stopping the Application

To stop the containers, run:

```bash
cd /home/ubuntu/server-monitor-devops
docker-compose down
```

---

## Troubleshooting

* **Port Binding Errors:** Ensure no other services are running on ports `5000`, `3000`, or `9090`.
* **Container Not Starting:** Check the logs using:

  ```bash
  docker logs <container_name>
  ```
* **Grafana Reconfiguration:** If Grafana prompts for setup each time, ensure the `grafana_data` volume is properly configured.

---

That’s it! You are now ready to monitor your application using Prometheus and visualize the data using Grafana.
