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
