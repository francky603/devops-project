pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                git url: 'git@github.com:francky603/devops-project.git', branch: 'main', credentialsId: 'github-ssh-key'
                echo 'Source code checked out successfully.'
            }
        }

        stage('Build Docker Images') {
            steps {
                dir('.') {
                    script {
                        echo 'Building Docker images for all services...'
                        sh 'docker-compose -f worker/docker-compose.yml build'
                    }
                }
            }
        }

        stage('Push Docker Images') {
            steps {
                dir('.') {
                    script {
                        echo 'Pushing Docker images to Docker Hub...'
                        withCredentials([usernamePassword(credentialsId: 'docker-hub-credentials', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                            sh 'echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin'
                            sh 'docker-compose -f worker/docker-compose.yml push'
                        }
                    }
                }
            }
        }

        stage('Deploy Application') {
            steps {
                dir('.') {
                    script {
                        echo 'Deploying the application stack...'
                        sh 'docker-compose -f worker/docker-compose.yml up -d'
                    }
                }
            }
        }

        stage('Verify Deployment') {
            steps {
                dir('.') {
                    script {
                        echo 'Verifying the status of deployed services...'
                        sh 'docker-compose -f worker/docker-compose.yml ps'
                        sleep(time: 10, unit: 'SECONDS')
                        echo 'Deployment verification complete.'
                    }
                }
            }
        }
    }

    post {
        always {
            emailext (
                subject: "Jenkins Pipeline Status: ${currentBuild.currentResult}",
                body: "Build ${currentBuild.fullDisplayName} completed with status ${currentBuild.currentResult}.\n\nCheck console output at \$BUILD_URL to view the results.",
                to: "m39624112@gmail.com",
                from: "m39624112@gmail.com"
            )
            echo 'Pipeline finished. Cleaning up workspace.'
        }
    }
}
