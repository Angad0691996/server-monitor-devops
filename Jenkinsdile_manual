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
                    ssh -o StrictHostKeyChecking=no -i \$KEY_FILE $EC2_USER@$EC2_HOST "
                        # Check if the directory exists; if not, clone the repository
                        if [ ! -d \"/home/ubuntu/server-monitor-devops/.git\" ]; then
                            cd /home/ubuntu
                            git clone https://github.com/Angad0691996/server-monitor-devops.git
                        else
                            cd /home/ubuntu/server-monitor-devops
                            git pull origin main
                        fi
                        
                        # Deploy with Docker Compose
                        cd /home/ubuntu/server-monitor-devops
                        docker-compose down
                        docker-compose up -d
                        docker system prune -f
                    "
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
