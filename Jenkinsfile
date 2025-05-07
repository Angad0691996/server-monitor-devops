pipeline {
    agent any

    environment {
        // Define Docker image names
        FLASK_IMAGE = 'flask_app'  // Update this to your Flask image name
        PROMETHEUS_IMAGE = 'prom/prometheus'
        GRAFANA_IMAGE = 'grafana/grafana'
    }

    stages {
        stage('Build Docker Images') {
            steps {
                script {
                    // Build Flask App Docker Image
                    sh 'docker build -t $FLASK_IMAGE .'
                }
            }
        }

        stage('Start Docker Containers') {
            steps {
                script {
                    // Start Prometheus container
                    sh 'docker run -d --name prometheus -p 9090:9090 $PROMETHEUS_IMAGE'

                    // Start Grafana container
                    sh 'docker run -d --name grafana -p 3000:3000 -e GF_SECURITY_ADMIN_PASSWORD=admin $GRAFANA_IMAGE'

                    // Start Flask app container
                    sh 'docker run -d --name server-monitor -p 5000:5000 $FLASK_IMAGE'
                }
            }
        }

        stage('Run Tests/Monitoring') {
            steps {
                script {
                    // Add commands to run tests or any other necessary monitoring here
                    echo 'Running tests or monitoring...'
                }
            }
        }

        stage('Stop Docker Containers') {
            steps {
                script {
                    // Stop and remove the containers after the tests or monitoring
                    sh 'docker stop server-monitor prometheus grafana'
                    sh 'docker rm server-monitor prometheus grafana'
                }
            }
        }
    }

    post {
        always {
            // Clean up any running containers if they were not stopped in the 'Stop Docker Containers' stage
            sh 'docker ps -q | xargs docker stop'
            sh 'docker ps -aq | xargs docker rm'
        }
    }
}
