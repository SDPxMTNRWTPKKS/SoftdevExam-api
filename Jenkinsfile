pipeline {
    triggers {
        pollSCM('H/1 * * * *') // ตรวจสอบทุก 1 นาที
    }
    agent { label 'connect-vmtest' }
    environment {

        GITLAB_IMAGE_NAME = "registry.gitlab.com/watthachai/simple-api-docker-registry" 
        VMTEST_MAIN_WORKSPACE = "/home/vmtest/workspace/ExamSoftdev"
        DOCKER_PORT = "5000" // ระบุ port ที่ต้องใช้
    
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
                        
                        # Clone repository สำหรับ robot test
                        rm -rf SoftdevExam-robot
                        git clone https://github.com/SDPxMTNRWTPKKS/SoftdevExam-robot.git || true
                        
                        # ติดตั้ง dependencies
                        cd ${VMTEST_MAIN_WORKSPACE}
                        pip install -r requirements.txt
                        
                        # รัน unit tests พร้อม coverage
                        python3 -m unittest unit_test.py -v
                        coverage run -m unittest unit_test.py -v
                        coverage report -m
                        
                        # รัน robot tests (ใน repository ที่ clone มาแล้ว)
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
        stage("Delivery to GitLab Registry") {
            agent {label 'connect-vmtest'}
            steps {
                withCredentials(
                    [usernamePassword(
                        credentialsId: 'gitlab-admin',
                        passwordVariable: 'gitlabPassword',
                        usernameVariable: 'gitlabUser'
                    )]
                ) {
                    sh "docker login registry.gitlab.com -u ${gitlabUser} -p ${gitlabPassword}"
                    sh "docker tag ${GITLAB_IMAGE_NAME} ${GITLAB_IMAGE_NAME}:${env.BUILD_NUMBER}"
                    sh "docker push ${GITLAB_IMAGE_NAME}:${env.BUILD_NUMBER}"
                    sh "docker rmi ${GITLAB_IMAGE_NAME}:${env.BUILD_NUMBER}"
                }
            }
        }
    }
}
