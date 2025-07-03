# Server Monitor DevOps - Automated Deployment

This project sets up a monitoring stack with Prometheus, Grafana, and a Flask-based server monitor using Docker Compose and Jenkins for automated deployment.

---

## Prerequisites

Ensure the following are installed on your EC2 instance:

* Docker
* Docker Compose
* Git
* Jenkins

---

## Project Structure

```
server-monitor-devops/
├── app/
│   └── run.py
├── docker-compose.yml
├── prometheus/
│   └── prometheus.yml
├── grafana_data/
├── requirements.txt
└── Jenkinsfile
```

---

## Setup and Deployment

1. **Clone the repository:**

```bash
cd /home/ubuntu
git clone https://github.com/Angad0691996/server-monitor-devops.git
cd server-monitor-devops
```

2. **Automated Deployment:**

* Push changes to the repository to trigger the Jenkins pipeline.
* The pipeline will build the Docker images and redeploy the containers automatically.

3. **Starting the Application:**

* Rebooting the EC2 instance will also restart the containers automatically via the pipeline.

---

## Accessing the Services

* Prometheus: `http://<EC2_IP>:9090`
* Grafana: `http://<EC2_IP>:3000`

  * Default credentials: `admin/admin`

---

## Stopping the Application

```bash
cd /home/ubuntu/server-monitor-devops
docker-compose down
```

---

## Troubleshooting

* Check Jenkins logs for pipeline status.
* Verify Docker container statuses using:

```bash
docker ps -a
```

That’s it! The deployment is now fully automated.
![image](https://github.com/user-attachments/assets/fe75696f-7e35-48c7-a3c4-110c70525c43)

