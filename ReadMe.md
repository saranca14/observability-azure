# Project Repository

This repository contains the source code and infrastructure for two applications: `shopping-app` and `voting-app`. It also includes configurations for DevOps tools and observability.

## Repository Structure

### Applications

- **Shopping App**: Contains the frontend and backend services for the shopping application.
  - `frontend/`: Frontend application code.
  - `orders/`, `payment/`, `products/`, `recommendations/`: Backend services.

- **Voting App**: Contains the services for the voting application.
  - `result/`, `seed-data/`, `vote/`, `worker/`: Various components of the voting application.

### DevOps

- **Ansible**: Configuration management and deployment scripts.
  - `ansible-playbook.log`, `ansible.cfg`, `app.py`, `inventory/`, `playbooks/`, `roles/`: Ansible configurations and playbooks.

- **Kubernetes**: Kubernetes manifests and configurations.
  - `common/`, `observability/`, `shopping-app/`, `voting-app/`: Kubernetes configurations for different applications and common resources.

- **Terraform**: Infrastructure as code using Terraform.
  - `infrastructure/`: Terraform configurations for infrastructure setup.

### Extras

- **otel-collector-extended**: OpenTelemetry Collector configurations.
  - `configmap.yaml`, `deployment.yaml`, `otel-rbac.yaml`, `pvc.yaml`, `service.yaml`: Kubernetes manifests for OpenTelemetry Collector.

## OpenTelemetry Workshop

This repository is also used for an OpenTelemetry workshop. The workshop aims to demonstrate how to implement observability in microservices using OpenTelemetry.

### Workshop Objectives

- Understand the basics of OpenTelemetry.
- Instrument applications for tracing, metrics, and logging.
- Deploy and configure OpenTelemetry Collector.
- Visualize telemetry data using tools like Prometheus and Grafana.

### Workshop Setup

1. **Clone the repository**:
   ```sh
   git clone https://github.com/your-repo.git
   cd your-repo


Set up the environment:

Ensure you have the prerequisites installed: Python, Ansible, Kubernetes, Terraform.
Deploy the applications:

Follow the instructions in the devops/kubernetes directory to deploy the shopping-app and voting-app on a Kubernetes cluster.
Configure OpenTelemetry:

Navigate to the extras/otel-collector-extended directory.
Apply the Kubernetes manifests to deploy the OpenTelemetry Collector:

kubectl apply -f configmap.yaml
kubectl apply -f deployment.yaml
kubectl apply -f otel-rbac.yaml
kubectl apply -f pvc.yaml
kubectl apply -f service.yaml



Getting Started
Prerequisites
Python
Ansible
Kubernetes
Terraform
Setting Up
Clone the repository:

Follow the instructions in the respective directories to set up and run the applications.