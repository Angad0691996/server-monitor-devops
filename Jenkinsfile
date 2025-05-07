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
                withCredentials([sshUserPrivateKey(credentialsId: 'ubuntu-ki-key', keyFileVariable: 'KEY_FILE')]) {
                    sh """
                    chmod 400 \$KEY_FILE
                    ssh -o StrictHostKeyChecking=no -i \$KEY_FILE $EC2_USER@$EC2_HOST << 'EOF'
                        cd /home/ubuntu/server-monitor-devops
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
