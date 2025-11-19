pipeline {
    agent any

    environment {
        ARM_SUBSCRIPTION_ID = credentials('ARM_SUBSCRIPTION_ID')
        ARM_CLIENT_ID       = credentials('ARM_CLIENT_ID')
        ARM_CLIENT_SECRET   = credentials('ARM_CLIENT_SECRET')
        ARM_TENANT_ID       = credentials('ARM_TENANT_ID')
        SSH_PUBLIC_KEY      = credentials('SSH_PUBLIC_KEY')
        TF_WORKING_DIR      = "terraform"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Terraform Init') {
            steps {
                dir("${TF_WORKING_DIR}") {
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
                dir("${TF_WORKING_DIR}") {
                    sh """
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
                dir("${TF_WORKING_DIR}") {
                    sh 'terraform apply -auto-approve tfplan'
                }
            }
        }
    }
}