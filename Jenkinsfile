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
                sh '''
                chmod 400 $KEY_FILE
                ssh -o StrictHostKeyChecking=no -i $KEY_FILE $EC2_USER@$EC2_HOST << 'EOF'
                    # Navigate to the deployment directory
                    cd /home/ubuntu/server-monitor-devops || {
                        echo 'Cloning repository...'
                        git clone https://github.com/Angad0691996/server-monitor-devops.git /home/ubuntu/server-monitor-devops
                        cd /home/ubuntu/server-monitor-devops
                    }

                    # Pull the latest changes
                    git pull origin main

                    # Check Docker installation
                    if ! command -v docker &> /dev/null; then
                        echo 'Docker not found, installing...'
                        sudo apt-get update
                        sudo apt-get install -y docker.io
                    fi

                    # Check Docker Compose installation
                    if ! command -v docker-compose &> /dev/null; then
                        echo 'Docker Compose not found, installing...'
                        sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.3/docker-compose-linux-x86_64" -o /usr/local/bin/docker-compose
                        sudo chmod +x /usr/local/bin/docker-compose
                    fi

                    # Deploy using Docker Compose
                    docker-compose down
                    docker-compose up -d

                    # Clean up unused Docker resources
                    docker system prune -f
                EOF
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