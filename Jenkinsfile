pipeline {

    agent {
        label 'docker-agent'
    }

    options {
        timestamps()
        timeout(time: 20, unit: 'MINUTES')
        disableConcurrentBuilds()
        buildDiscarder(logRotator(numToKeepStr: '20'))
    }

    environment {
        IMAGE_NAME   = "demo-app"
        REGISTRY_URL = "https://registry.example.com"
        IMAGE_TAG    = "${env.BUILD_NUMBER}"
        DEPLOY_HOST  = "192.168.1.20"
    }

    parameters {
        booleanParam(name: 'SKIP_SCAN', defaultValue: false, description: 'Ignorer le scan de sécurité (dépannage uniquement)')
        string(name: 'DEPLOY_ENV', defaultValue: 'staging', description: 'Environnement cible')
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build & Unit Tests') {
            steps {
                sh 'pip install -r app/requirements.txt'
                sh 'python -m py_compile app/app.py'
            }
        }

        stage('Docker Build') {
            steps {
                script {
                    docker.build("${env.IMAGE_NAME}:${env.IMAGE_TAG}")
                }
            }
        }

        stage('Image Scan') {
            when {
                expression { return !params.SKIP_SCAN }
            }
            steps {
                sh "trivy image --exit-code 1 --severity HIGH,CRITICAL ${env.IMAGE_NAME}:${env.IMAGE_TAG}"
            }
        }

        stage('Docker Push') {
            steps {
                script {
                    docker.withRegistry(env.REGISTRY_URL, 'docker-registry-credentials') {
                        def image = docker.image("${env.IMAGE_NAME}:${env.IMAGE_TAG}")
                        image.push()
                    }
                }
            }
        }

        stage('Deploy') {
            steps {
                withCredentials([sshUserPrivateKey(credentialsId: 'docker-deploy-ssh', keyFileVariable: 'SSH_KEY')]) {
                    sh '''
                        ssh -i $SSH_KEY -o StrictHostKeyChecking=no jenkins-deploy@${DEPLOY_HOST} "
                            docker pull registry.example.com/${IMAGE_NAME}:${IMAGE_TAG} &&
                            docker stop ${IMAGE_NAME} || true &&
                            docker rm ${IMAGE_NAME} || true &&
                            docker run -d --name ${IMAGE_NAME} --restart unless-stopped -p 8080:8080 \
                                registry.example.com/${IMAGE_NAME}:${IMAGE_TAG}
                        "
                    '''
                }
            }
        }

        stage('Health Check') {
            steps {
                sh "curl -f http://${DEPLOY_HOST}:8080/health"
            }
        }

        stage('Cleanup') {
            steps {
                sh "docker image prune -f"
            }
        }

    }

    post {
        success {
            echo "Build ${env.IMAGE_TAG} déployé avec succès sur ${params.DEPLOY_ENV}."
        }
        failure {
            echo "Échec du build ${env.IMAGE_TAG} — voir Console Output pour le détail."
        }
        always {
            cleanWs()
        }
    }
}
