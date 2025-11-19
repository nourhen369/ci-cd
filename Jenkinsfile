pipeline {
    agent any

    environment {
        TF_DIR = 'terraform'
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Terraform Init') {
            steps {
                withCredentials([
                    string(credentialsId: 'azure-subscription-id', variable: 'ARM_SUBSCRIPTION_ID'),
                    string(credentialsId: 'azure-client-id',       variable: 'ARM_CLIENT_ID'),
                    string(credentialsId: 'azure-client-secret',   variable: 'ARM_CLIENT_SECRET'),
                    string(credentialsId: 'azure-tenant-id',       variable: 'ARM_TENANT_ID')
                ]) {
                    sh '''
                        set -euo pipefail
                        cd ${TF_DIR}
                        terraform init -input=false
                        terraform validate || true
                        terraform plan -out=tfplan -input=false
                        terraform apply -auto-approve tfplan
                    '''
                }
            }
        }

        stage('Generate Ansible Inventory') {
            steps {
                sh '''
                    set -euo pipefail
                    cd ${TF_DIR}
                    VM_IP=$(terraform output -raw vm_public_ip)
                    echo "[web]" > ../inventory.ini
                    echo "${VM_IP} ansible_user=azureuser" >> ../inventory.ini
                    cd ..
                    ls -l inventory.ini
                    cat inventory.ini
                '''
            }
        }

        stage('Run Ansible Playbook') {
            steps {
                withCredentials([
                    sshUserPrivateKey(
                        credentialsId: 'jenkins-ssh-key',
                        keyFileVariable: 'SSH_KEY_FILE',
                        usernameVariable: 'SSH_USER'
                    )
                ]) {
                    sh '''
                        set -euo pipefail
                        chmod 600 "$SSH_KEY_FILE"

                        /opt/ansible-venv/bin/ansible-playbook -i inventory.ini playbook.yml \
                        --private-key "$SSH_KEY_FILE" -u "$SSH_USER" \
                        -e "ansible_python_interpreter=/usr/bin/python3"
                    '''
                }
            }
        }
    }

    post {
        success {
            echo 'Pipeline terminé avec succès — infra provisionnée et app déployée.'
        }
        failure {
            echo 'Pipeline échoué — vérifier les logs et les permissions.'
        }
    }
}