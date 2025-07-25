pipeline {
    agent any
    environment {
        DOCKERHUB_CREDENTIALS = credentials("dockerhub")
        DOCKERHUB_USERNAME = "franky0777"
        DOCKER_BUILDKIT = "1"
    }
    stages {
        stage("Clone Repository") {
            steps {
                git "https://github.com/francky603/devops-project.git"
            }
        }
        stage("Build Docker Images") {
            steps {
                sh "docker-compose build"
            }
        }
        stage("SonarQube Analysis") {
            steps {
                script {
                    def scannerHome = tool "SonarQubeScanner"
                    withSonarQubeEnv("SonarQube") {
                        sh "${scannerHome}/bin/sonar-scanner -Dsonar.projectKey=voting-app -Dsonar.sources=vote,result,worker"
                    }
                }
            }
        }
        stage("Push to Docker Hub") {
            steps {
                script {
                    sh "echo $DOCKERHUB_CREDENTIALS_PSW | docker login -u $DOCKERHUB_CREDENTIALS_USR --password-stdin"
                    sh "docker-compose push"
                }
            }
        }
        stage("Deploy") {
            steps {
                sh "docker-compose up -d --remove-orphans"
            }
        }
        stage("Verify Deployment") {
            steps {
                sh "docker-compose ps"
                sh "curl --insecure --retry 5 --retry-delay 5 https://localhost:5000 || exit 1"
                sh "curl --insecure --retry 5 --retry-delay 5 https://localhost:5001 || exit 1"
            }
        }
    }
    post {
        success {
            mail to: "m39624112@gmail.com",
                 subject: "Pipeline Success: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                 body: "The pipeline ${env.JOB_NAME} completed successfully. Access vote at https://<server-ip>:5000 and result at https://<server-ip>:5001."
        }
        failure {
            mail to: "m39624112@gmail.com",
                 subject: "Pipeline Failed: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                 body: "The pipeline ${env.JOB_NAME} failed. Check Jenkins logs at http://<server-ip>:8080/job/${env.JOB_NAME}/${env.BUILD_NUMBER}/console."
        }
    }
}
