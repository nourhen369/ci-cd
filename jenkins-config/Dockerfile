FROM jenkins/jenkins:lts

USER root
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get upgrade -y && \
    apt-get install -y --no-install-recommends \
        ca-certificates \
        curl \
        gnupg \
        gpg \
        lsb-release \
        apt-transport-https \
        software-properties-common \
        docker.io \
        python3 \
        python3-pip \
        sudo \
        unzip && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

RUN curl -fsSL https://apt.releases.hashicorp.com/gpg | gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg && \
    echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" > /etc/apt/sources.list.d/hashicorp.list && \
    apt-get update && apt-get install -y terraform && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

RUN curl -sL https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor -o /usr/share/keyrings/microsoft-archive-keyring.gpg && \
    echo "deb [arch=amd64 signed-by=/usr/share/keyrings/microsoft-archive-keyring.gpg] https://packages.microsoft.com/repos/azure-cli/ $(lsb_release -cs) main" > /etc/apt/sources.list.d/azure-cli.list && \
    apt-get update && apt-get install -y azure-cli && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

RUN DOCKER_COMPOSE_VERSION=2.20.2 && \
    mkdir -p /usr/lib/docker/cli-plugins && \
    curl -fsSL "https://github.com/docker/compose/releases/download/v${DOCKER_COMPOSE_VERSION}/docker-compose-linux-x86_64" -o /usr/lib/docker/cli-plugins/docker-compose && \
    chmod +x /usr/lib/docker/cli-plugins/docker-compose

# Créer un virtualenv pour Ansible
RUN apt-get update && apt-get install -y python3 python3-venv python3-pip
RUN python3 -m venv /opt/ansible-venv
RUN /opt/ansible-venv/bin/pip install --upgrade pip ansible
ENV PATH="/opt/ansible-venv/bin:$PATH"

RUN usermod -aG docker jenkins
USER jenkins