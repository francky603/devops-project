pipeline {
    agent any
    environment {
        DOCKERHUB_CREDENTIALS = credentials('dockerhub')
        DOCKERHUB_USERNAME = 'franky0777'
    }
    stages {
        stage('Clone Repository') {
            steps {
                git 'https://github.com/inaleoby/devops-project.git'
            }
        }
        stage('Build Docker Images') {
            steps {
                sh 'docker compose build'
            }
        }
        stage('SonarQube Analysis') {
            steps {
                script {
                    def scannerHome = tool 'SonarQubeScanner'
                    withSonarQubeEnv('SonarQube') {
                        sh "${scannerHome}/bin/sonar-scanner -Dsonar.projectKey=voting-app -Dsonar.sources=vote,result,worker"
                    }
                }
            }
        }
        stage('Push to Docker Hub') {
            steps {
                sh 'echo $DOCKERHUB_CREDENTIALS_PSW | docker login -u $DOCKERHUB_CREDENTIALS_USR --password-stdin'
                sh 'docker compose push'
            }
        }
        stage('Deploy') {
            steps {
                sh 'docker compose up -d --remove-orphans'
            }
        }
        stage('Verify Deployment') {
            steps {
                sh 'docker compose ps'
                sh 'curl http://localhost:5000' // Vote service
                sh 'curl http://localhost:5001' // Result service
            }
        }
    }
    post {
        success {
            mail to: 'm39624112@gmail.com',
                 subject: "Pipeline Success: ${env.JOB_NAME}",
                 body: "The pipeline ${env.JOB_NAME} completed successfully. Access at http://<server-ip>:5000 (vote) and http://<server-ip>:5001 (result)."
        }
        failure {
            mail to: 'm39624112@gmail.com',
                 subject: "Pipeline Failed: ${env.JOB_NAME}",
                 body: "The pipeline ${env.JOB_NAME} failed. Check Jenkins logs for details."
        }
    }
}
