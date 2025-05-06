pipeline {
    agent any
    environment {
        // Define the EC2 SSH key and remote server details
        EC2_HOST = 'your-ec2-ip'
        EC2_USER = 'ubuntu'
        SSH_KEY = credentials('ubuntu-ki-key') // Use your EC2 SSH key credential ID here
        GIT_CREDENTIALS = credentials('github-creds') // Use your GitHub access token credential ID here
    }
    stages {
        stage('Checkout') {
            steps {
                // Clone the repository from GitHub using the GitHub access token
                git url: 'https://github.com/Angad0691996/server-monitor-devops.git', credentialsId: 'github-creds'
            }
        }

        stage('Build Docker Images') {
            steps {
                script {
                    // Build the Docker images using Docker Compose
                    sh 'docker-compose -f docker-compose.yml build'
                }
            }
        }

        stage('Deploy to EC2') {
            steps {
                script {
                    // Deploy Docker containers (Prometheus, Grafana, and Flask) to EC2
                    sh """
                    ssh -i $SSH_KEY $EC2_USER@$EC2_HOST << 'EOF'
                        cd /path/to/your/project
                        docker-compose down
                        docker-compose up -d
                    EOF
                    """
                }
            }
        }

        stage('Grafana Access') {
            steps {
                script {
                    // Check if Grafana is accessible
                    echo "Grafana is now accessible at http://$EC2_HOST:3000"
                }
            }
        }

        stage('Clean Up') {
            steps {
                // Clean up any temporary files or containers if needed
                sh 'docker system prune -f'
            }
        }
    }
    post {
        always {
            // Always notify or clean up after the pipeline runs
            echo 'Pipeline execution complete!'
        }
    }
}
