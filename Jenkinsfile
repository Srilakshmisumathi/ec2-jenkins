pipeline {
    agent any

    environment {
        EC2_USER = "ubuntu"                  // Change to your EC2 user (e.g., ec2-user for Amazon Linux)
        EC2_HOST = "65.0.103.122"      // Replace with your EC2 instance IP
        APP_DIR = "/home/ubuntu/ec2-jenkins/app" // Path to app directory on EC2
        SSH_KEY = "/var/lib/jenkins/jenkins.pem"    // Path to your EC2 private key
        APP_PORT = "5000"                    // Flask application port
    }

    stages {
        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }

        stage('Deploy to EC2') {
    steps {
        script {
            echo "Copying updated application files to EC2..."
            sh '''
            scp -o StrictHostKeyChecking=no -i /var/lib/jenkins/jenkins.pem -r app/main.py app/templates ubuntu@65.0.103.122:/home/ubuntu/ec2-jenkins/app/
            '''
            
            echo "Restarting application on EC2..."
            sh '''
            ssh -o StrictHostKeyChecking=no -i /var/lib/jenkins/jenkins.pem ubuntu@65.0.103.122 <<EOF
            sudo pkill -f gunicorn || echo "Gunicorn process not found"
            cd /home/ubuntu/ec2-jenkins/app
            source /home/ubuntu/ec2-jenkins/venv/bin/activate
            nohup gunicorn -w 4 -b 0.0.0.0:5000 main:app > gunicorn.log 2>&1 &
            exit
EOF
            '''
        }
    }
}


}

    post {
        success {
            echo 'Deployment to EC2 successful!'
        }
        failure {
            echo 'Deployment failed. Check the logs for details.'
        }
    }
}
