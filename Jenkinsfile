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
                dir("${TF_DIR}") {
                    sh """
                        terraform init \
                        -backend-config="resource_group_name=TerraformStateRG" \
                        -backend-config="storage_account_name=tfstateaccount" \
                        -backend-config="container_name=tfstate" \
                        -backend-config="key=terraform.tfstate"
                    """
                }
            }
        }

        stage('Terraform Plan') {
            steps {
                withCredentials([
                    string(credentialsId: 'azure-subscription-id', variable: 'ARM_SUBSCRIPTION_ID'),
                    string(credentialsId: 'azure-client-id',       variable: 'ARM_CLIENT_ID'),
                    string(credentialsId: 'azure-client-secret',   variable: 'ARM_CLIENT_SECRET'),
                    string(credentialsId: 'azure-tenant-id',       variable: 'ARM_TENANT_ID'),
                    string(credentialsId: 'ssh-public-key',        variable: 'SSH_PUBLIC_KEY')
                ]) {
                    sh """
                        cd ${TF_DIR}
                        terraform plan -out=tfplan \
                        -var "subscription_id=${ARM_SUBSCRIPTION_ID}" \
                        -var "client_id=${ARM_CLIENT_ID}" \
                        -var "client_secret=${ARM_CLIENT_SECRET}" \
                        -var "tenant_id=${ARM_TENANT_ID}" \
                        -var "ssh_public_key=${SSH_PUBLIC_KEY}"
                    """
                }
            }
        }

        stage('Terraform Apply') {
            steps {
                dir("${TF_DIR}") {
                    sh 'terraform apply -auto-approve tfplan'
                }
            }
        }
    }
}