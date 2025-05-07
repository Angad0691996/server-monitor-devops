Server Monitor DevOps Setup (Automated)
Introduction
This project automates the deployment of a monitoring stack consisting of Prometheus, Grafana, and a Flask-based server monitor application using Jenkins, Docker Compose, and GitHub Webhooks. The setup allows you to monitor server metrics and visualize them using Grafana, with everything being redeployed automatically when changes are pushed to the repository.

Prerequisites
Ensure the following are installed and configured on your EC2 instance:

Docker

Docker Compose

Git

Jenkins (for CI/CD pipeline)

GitHub repository connected to Jenkins (via webhook)

SSH Keys for GitHub and Jenkins integration

Project Structure
bash
Copy
Edit
server-monitor-devops/
├── app/
│   └── run.py            # Flask application
├── docker-compose.yml    # Docker Compose configuration
├── prometheus/
│   └── prometheus.yml    # Prometheus configuration
├── grafana_data/         # Grafana data persistence (will be created)
├── requirements.txt      # Python dependencies
├── Jenkinsfile           # CI/CD pipeline configuration
└── docker-compose.yml    # Defines the containers for Flask, Prometheus, and Grafana
Setup and Configuration
1. Clone the Repository on the EC2 Instance
Clone the repository to your EC2 instance:

bash
Copy
Edit
cd /home/ubuntu
git clone https://github.com/Angad0691996/server-monitor-devops.git
cd server-monitor-devops
2. Configure Jenkins
Set up a Jenkins pipeline to automate the deployment:

Create a Jenkins pipeline job.

Link the job to your GitHub repository.

In the Jenkinsfile, use the following pipeline script (as described below) to automate the build and deployment process.

3. Jenkins Pipeline Script (Jenkinsfile)
groovy
Copy
Edit
pipeline {
    agent any
    environment {
        EC2_HOST = '13.202.247.39'  // Your EC2 instance IP
        EC2_USER = 'ubuntu'
        GIT_CREDENTIALS = credentials('github-creds')  // Add your GitHub credentials in Jenkins
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/Angad0691996/server-monitor-devops.git', credentialsId: 'github-creds'
            }
        }

        stage('Build Docker Images') {
            steps {
                sh 'docker-compose -f docker-compose.yml build'
            }
        }

        stage('Deploy to EC2') {
            steps {
                withCredentials([sshUserPrivateKey(credentialsId: 'jenkins-ubuntu-key', keyFileVariable: 'KEY_FILE')]) {
                    sh '''
                    chmod 600 $KEY_FILE  # Set correct permissions for the SSH key
                    ssh -o StrictHostKeyChecking=no -i $KEY_FILE $EC2_USER@$EC2_HOST "
                        # Pull the latest changes
                        cd /home/ubuntu/server-monitor-devops
                        git pull origin main

                        # Stop existing containers
                        docker-compose down

                        # Ensure the data volumes are created
                        docker volume create grafana_data

                        # Rebuild and deploy with Docker Compose
                        docker-compose up -d --build

                        # Prune unused images and containers
                        docker system prune -f
                    "
                    '''
                }
            }
        }

        stage('Grafana Access') {
            steps {
                echo "Grafana is now accessible at http://$EC2_HOST:3000"
            }
        }
    }

    post {
        always {
            echo 'Pipeline execution complete!'
        }
    }
}
This Jenkins pipeline will automatically:

Pull the latest code from GitHub on every commit.

Build Docker images and deploy the containers on the EC2 instance.

4. Configure GitHub Webhook
Go to your GitHub repository → Settings → Webhooks.

Add a new webhook:

Payload URL: http://<JENKINS_IP>/github-webhook/

Content Type: application/json

Which events would you like to trigger this webhook?: Select Just the push event.

Once this is set up, Jenkins will be triggered automatically every time a commit is made.

Starting the Application
Once Jenkins is set up and the GitHub webhook is configured:

Jenkins will automatically trigger the pipeline every time a commit is made to the repository.

The Docker containers will be redeployed on the EC2 instance without any manual intervention.

Accessing Prometheus and Grafana
Prometheus: http://<EC2_IP>:9090

Grafana: http://<EC2_IP>:3000

Default username: admin

Default password: admin

Stopping the Application
To stop the containers, the Jenkins pipeline will automatically run the following command after each deployment:

bash
Copy
Edit
docker-compose down
Troubleshooting
Port Binding Errors: Ensure no other services are running on ports 5000, 3000, or 9090.

Container Not Starting: Check the logs using:

bash
Copy
Edit
docker logs <container_name>
Grafana Reconfiguration: If Grafana prompts for setup each time, ensure the grafana_data volume is properly configured and mounted.

Auto Start After EC2 Reboot
To ensure that the services start automatically after an EC2 reboot, we’ve added a Docker restart policy (restart: always) in the docker-compose.yml file. This guarantees that all services (Flask, Prometheus, Grafana) are restarted automatically if the EC2 instance is rebooted.

Conclusion
With this setup, your server monitoring stack is fully automated! Jenkins will automatically redeploy your containers when changes are made to your repository, and Docker's restart policy ensures the services are up and running even after an EC2 reboot.