pipeline {
    triggers {
        pollSCM('H/1 * * * *') // Check every 1 minutes
    }
    agent { label 'connect-vmtest' }
    environment {
        GITLAB_IMAGE_NAME = "registry.gitlab.com/watthachai/simple-api-docker-registry"
        VMTEST_MAIN_WORKSPACE = "/home/vmtest/workspace/SDPx1@2"
        DOCKER_PORT = "5000" // Specify the port to use
    }
    stages {
        stage('Deploy Docker Compose') {
            agent { label 'connect-vmtest' }
            steps {
                sh "docker compose up -d --build"
            }
        }

        stage('Run Tests') {
            agent { label 'connect-vmtest' }
            steps {
                script {
                    try {
                        sh '''
                        . /home/vmtest/env/bin/activate
                        
                        # Clone and set up the test repository if not already cloned
                        rm -rf SoftdevExam-robot
                        git clone https://github.com/SDPxMTNRWTPKKS/SoftdevExam-robot.git || true
                        
                        # Install dependencies
                        cd ${VMTEST_MAIN_WORKSPACE}
                        pip install -r requirements.txt
                        
                        # Run unit tests with coverage
                        python3 -m unittest unit_test.py -v
                        coverage run -m unittest unit_test.py -v
                        coverage report -m
                        
                        # Run robot tests
                        cd SoftdevExam-robot
                        robot robot_test.robot || true
                        '''
                    } catch (Exception e) {
                        echo "Error during testing: ${e.getMessage()}"
                        currentBuild.result = 'FAILURE'
                        error("Tests failed!")
                    }
                }
            }
        }

        stage('Delivery to GitLab Registry') {
            agent { label 'connect-vmtest' }
            steps {
                script {
                    try {
                        withCredentials([usernamePassword(
                                credentialsId: 'gitlab-registry',
                                passwordVariable: 'gitlabPassword',
                                usernameVariable: 'gitlabUser'
                            )]
                        ) {
                            echo "Logging into GitLab registry..."
                            sh "docker login registry.gitlab.com -u ${gitlabUser} -p ${gitlabPassword}"
                            echo "Tagging and pushing Docker image..."
                            sh "docker tag ${GITLAB_IMAGE_NAME} ${GITLAB_IMAGE_NAME}:${env.BUILD_NUMBER}"
                            sh "docker push ${GITLAB_IMAGE_NAME}:${env.BUILD_NUMBER}"
                            sh "docker rmi ${GITLAB_IMAGE_NAME}:${env.BUILD_NUMBER}"
                        }
                    } catch (Exception e) {
                        echo "Error during delivery: ${e.getMessage()}"
                        currentBuild.result = 'FAILURE'
                        error("Delivery to GitLab registry failed!")
                    }
                }
            }
        }

        stage("Pull from GitLab Registry") {
            agent {label 'connect-vmpreprod'}
            steps {
                withCredentials(
                    [usernamePassword(
                        credentialsId: 'gitlab-registry',
                        passwordVariable: 'gitlabPassword',
                        usernameVariable: 'gitlabUser'
                    )]
                ) {
                    script {
                        def containers = sh(script: "docker ps -q", returnStdout: true).trim()
                        if (containers) {
                            sh "docker stop ${containers}"
                        } else {
                            echo "No running containers to stop."
                        }
                    }
                    sh "docker login registry.gitlab.com -u ${gitlabUser} -p ${gitlabPassword}"
                    sh "docker pull ${GITLAB_IMAGE_NAME}:${env.BUILD_NUMBER}"
                    sh "docker run -p 5000:5000 -d ${GITLAB_IMAGE_NAME}:${env.BUILD_NUMBER}"
                }
            }
        }
        
    }
}