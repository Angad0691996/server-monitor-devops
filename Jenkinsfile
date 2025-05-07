pipeline {
    agent any
    environment {
        EC2_HOST = '13.127.116.15'  
        EC2_USER = 'ubuntu'
        GIT_CREDENTIALS = credentials('github-creds')
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
                    sh """
                    chmod 600 \$KEY_FILE  # Set correct permissions for the SSH key
                    ssh -o StrictHostKeyChecking=no -i \$KEY_FILE $EC2_USER@$EC2_HOST << 'EOF'
                        # Ensure the directory exists
                        mkdir -p /home/ubuntu/server-monitor-devops
                        cd /home/ubuntu/server-monitor-devops
                        
                        # Pull latest changes from GitHub if necessary
                        git pull origin main
                        
                        # Deploy with Docker Compose
                        docker-compose down
                        docker-compose up -d
                        docker system prune -f
                    EOF
                    """
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
