// pipeline {
//     agent any

//     environment {
//         BACKEND_DIR   = "backend"
//         FRONTEND_DIR  = "frontend"
//         DOCKER_IMAGE_BACKEND  = "${env.DOCKER_REGISTRY ?: 'my-registry.example.com'}/integraite-backend"
//         DOCKER_IMAGE_FRONTEND = "${env.DOCKER_REGISTRY ?: 'my-registry.example.com'}/integraite-frontend"
//         COMMIT_SHA = "${env.GIT_COMMIT ?: 'dev'}"
//         PYTHON = "python3"
//         NODE_VERSION = "20"
//     }

//     // options {
//     //     timestamps()
//     //     ansiColor('xterm')
//     // }

//     stages {
//         stage('Checkout') {
//             steps {
//                 checkout scm
//             }
//         }

//         stage('Set Up Runtimes') {
//             steps {
//                 script {
//                     // timestamps {
//                     //     ansiColor('xterm') {
//                             sh "${PYTHON} --version"
//                             sh "node --version || nvm use ${NODE_VERSION}"
//                     //     }
//                     // }
//                 }
//             }
//         }

//         stage('Install Backend Dependencies') {
//             steps {
//                 script {
//                     // timestamps {
//                     //     ansiColor('xterm') {
//                             dir(BACKEND_DIR) {
//                                 sh "${PYTHON} -m pip install --upgrade pip"
//                                 sh "${PYTHON} -m pip install -r requirements.txt"
//                             }
//                     //     }
//                     // }
//                 }
//             }
//         }

//         stage('Install Frontend Dependencies') {
//             steps {
//                 script {
//                     // timestamps {
//                     //     ansiColor('xterm') {
//                             dir(FRONTEND_DIR) {
//                                 sh 'npm ci'
//                             }
//                     //     }
//                     // }
//                 }
//             }
//         }

//         stage('Run Tests') {
//             parallel {
//                 stage('Backend Tests') {
//                     steps {
//                         dir(BACKEND_DIR) {
//                             sh 'pytest'
//                         }
//                     }
//                 }
//                 stage('Frontend Tests') {
//                     steps {
//                         dir(FRONTEND_DIR) {
//                             sh 'CI=true npm test -- --watch=false'
//                         }
//                     }
//                 }
//             }
//         }

//         stage('Build Docker Images') {
//             steps {
//                 script {
//                     // timestamps {
//                     //     ansiColor('xterm') {
//                             sh "docker build -t ${DOCKER_IMAGE_BACKEND}:${COMMIT_SHA} ${BACKEND_DIR}"
//                             sh "docker build -t ${DOCKER_IMAGE_FRONTEND}:${COMMIT_SHA} ${FRONTEND_DIR}"
//                     //     }
//                     // }
//                 }
//             }
//         }

//         stage('Push Docker Images') {
//             when { expression { env.DOCKERHUB_CREDENTIALS } }
//             steps {
//                 script {
//                     // timestamps {
//                     //     ansiColor('xterm') {
//                             withCredentials([usernamePassword(credentialsId: env.DOCKERHUB_CREDENTIALS, usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
//                                 sh 'echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin ${DOCKER_REGISTRY ?: ""}'
//                                 sh "docker push ${DOCKER_IMAGE_BACKEND}:${COMMIT_SHA}"
//                                 sh "docker push ${DOCKER_IMAGE_FRONTEND}:${COMMIT_SHA}"
//                             }
//                     //     }
//                     // }
//                 }
//             }
//         }

//         stage('Deploy') {
//             when { expression { env.DEPLOY_ENABLED == 'true' } }
//             steps {
//                 script {
//                     // timestamps {
//                     //     ansiColor('xterm') {
//                             sh './scripts/deploy.sh'
//                     //     }
//                     // }
//                 }
//             }
//         }
//     }

//     // post {
//     //     always {
//     //         // cleanWs()
//     //     }
//     // }
// }
pipeline {
    agent any

    environment {
        BACKEND_DIR   = "backend"
        FRONTEND_DIR  = "frontend"
        DOCKER_REGISTRY_USER = "batshevamalkarechnitzer" 
        DOCKER_IMAGE_BACKEND  = "${DOCKER_REGISTRY_USER}/integraite-backend"
        DOCKER_IMAGE_FRONTEND = "${DOCKER_REGISTRY_USER}/integraite-frontend"
        COMMIT_SHA = "${env.GIT_COMMIT ?: 'dev'}"
        // כאן הגדירי את ה-ID של ה-Credentials שיצרת בג'נקינס עבור Docker Hub
        DOCKERHUB_CREDENTIALS = "docker-hub-creds" 
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Backend Build & Test') {
            steps {
                script {
                    // בניית האימג' (הקוד כבר בפנים, אין צורך במיפוי תיקיות שנכשל)
                    sh "docker build -t ${DOCKER_IMAGE_BACKEND}:${COMMIT_SHA} ./${BACKEND_DIR}"
                    
                    // הרצת הבדיקות בתוך האימג' שנבנה
                    sh "docker run --rm ${DOCKER_IMAGE_BACKEND}:${COMMIT_SHA} pytest"
                }
            }
        }

        stage('Frontend Build & Test') {
            steps {
                script {
                    // 1. בניית אימג' זמני לעצירה בשלב ה-Node (חייב AS build ב-Dockerfile)
                    sh "docker build --target build -t frontend-test-env ./${FRONTEND_DIR}"
                    
                    // 2. הרצת בדיקות (CI=true מונע מהטסטים להיתקע)
                    sh "docker run --rm -e CI=true frontend-test-env npm test -- --watchAll=false"
                    
                    // 3. אם עבר - בניית האימג' הסופי והרזה (Nginx) ישר עם השם המלא
                    sh "docker build -t ${DOCKER_IMAGE_FRONTEND}:${COMMIT_SHA} ./${FRONTEND_DIR}"
                }
            }
        }

        stage('Push Docker Images') {
            // השלב הזה ירוץ רק אם הגדרת Credentials בג'נקינס
            when { expression { env.DOCKERHUB_CREDENTIALS != '' } }
            steps {
                script {
                    withCredentials([usernamePassword(credentialsId: env.DOCKERHUB_CREDENTIALS, usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                        sh 'echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin'
                        sh "docker push ${DOCKER_IMAGE_BACKEND}:${COMMIT_SHA}"
                        sh "docker push ${DOCKER_IMAGE_FRONTEND}:${COMMIT_SHA}"
                    }
                }
            }
        }

        stage('Deploy') {
            // שלב זה ירוץ רק אם תגדירי משתנה DEPLOY_ENABLED כ-true
            // when { expression { env.DEPLOY_ENABLED == 'true' } }
            steps {
                // ודאי שהסקריפט קיים בנתיב הזה ב-Git
                sh 'chmod +x ./scripts/deploy.sh'
                sh './scripts/deploy.sh'
            }
        }
    }
}