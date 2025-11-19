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

        stage('Terraform Apply') {
            steps {
                withCredentials([
                    "ARM_SUBSCRIPTION_ID=$ARM_SUBSCRIPTION_ID",
                    "ARM_CLIENT_ID=$ARM_CLIENT_ID",
                    "ARM_CLIENT_SECRET=$ARM_CLIENT_SECRET",
                    "ARM_TENANT_ID=$ARM_TENANT_ID",
                    "SSH_PUBLIC_KEY=$SSH_PUBLIC_KEY"
                ]) {
                    sh """
                    bash -c '
                    set -euo pipefail
                    cd ${TF_DIR}
                    terraform init -input=false
                    terraform plan -out=tfplan -input=false -var "subscription_id=$ARM_SUBSCRIPTION_ID" -var "client_id=$ARM_CLIENT_ID" -var "client_secret=$ARM_CLIENT_SECRET" -var "tenant_id=$ARM_TENANT_ID" -var "ssh_public_key=$SSH_PUBLIC_KEY"
                    terraform apply -auto-approve tfplan
                    '
                    """
                }
            }
        }

        stage('Generate Ansible Inventory') {
            steps {
                sh 'bash -c "set -euo pipefail; cd ${TF_DIR}; VM_IP=$(terraform output -raw vm_public_ip); echo \"[web]\" > ../inventory.ini; echo \"${VM_IP} ansible_user=azureuser\" >> ../inventory.ini"'
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
                    sh 'bash -c "set -euo pipefail; chmod 600 \$SSH_KEY_FILE; /opt/ansible-venv/bin/ansible-playbook -i inventory.ini playbook.yml --private-key \$SSH_KEY_FILE -u \$SSH_USER -e \"ansible_python_interpreter=/usr/bin/python3\""'
                }
            }
        }
    }
}