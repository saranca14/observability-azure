# OpenTelemetry Demo: E-Commerce and Voting Applications

This repository contains a demonstration of using OpenTelemetry for observability in a distributed microservices environment.  It includes two applications:

*   **`shopping-app`:** A simplified e-commerce application with multiple microservices (frontend, orders, products, recommendations, payment).  This application uses **automatic** OpenTelemetry instrumentation.
*   **`voting-app`:** A simple voting application (result, vote, worker, seed-data). This application uses **manual** OpenTelemetry instrumentation.

Both applications are designed for deployment to Kubernetes (specifically Azure Kubernetes Service - AKS) and are instrumented to send traces, metrics, and logs to an OpenTelemetry Collector.  The collector then exports this data to various backends (Zipkin, Prometheus, Grafana, Loki, and optionally Azure Monitor).

## Table of Contents

1.  [Project Overview](#project-overview)
2.  [Architecture](#architecture)
3.  [Prerequisites](#prerequisites)
4.  [Setup and Installation](#setup-and-installation)
    *   [Clone the Repository](#clone-the-repository)
    *   [Install Dependencies](#install-dependencies)
    *   [Build Docker Images](#build-docker-images)
    *   [Push Docker Images](#push-docker-images)
    *   [Choose a Deployment Method](#choose-a-deployment-method)
        *   [Kubernetes (using `kubectl`)](#kubernetes-using-kubectl)
        *   [Terraform (Optional)](#terraform-optional)
        *   [Ansible (Optional)](#ansible-optional)
    *   [Create Kubernetes Namespace](#create-kubernetes-namespace)
    *   [Create Secrets (Optional but Recommended)](#create-secrets-optional-but-recommended)
    *   [Deploy to Kubernetes (kubectl)](#deploy-to-kubernetes-kubectl)
    *   [Deploy using Terraform (Optional)](#deploy-using-terraform-optional)
    *   [Deploy using Ansible (Optional)](#deploy-using-ansible-optional)
5.  [Verification and Testing](#verification-and-testing)
6.  [Observability Details](#observability-details)
7.  [Troubleshooting](#troubleshooting)
8.  [Cleaning Up](#cleaning-up)
9.  [Directory Structure](#directory-structure)
10. [Contributing](#contributing)
11. [Observability Concepts](#observability-concepts)

## 1. Project Overview

This project aims to provide a practical, hands-on demonstration of OpenTelemetry in a realistic microservices environment. It highlights the differences between automatic and manual instrumentation and showcases how to use a variety of observability backends.  The project structure also shows how to manage infrastructure and deployment using tools like Kubernetes, Terraform, and Ansible.

## 2. Architecture

**Application Components:**

*   **`shopping-app` (E-commerce - Auto-instrumented):**
    *   `frontend`:  Flask web application serving the UI.
    *   `orders`: Flask service for handling order placement.
    *   `payment`: Flask service simulating payment processing.
    *   `products`: Flask service providing product data.
    *   `recommendations`: Flask service for product recommendations.

*   **`voting-app` (Voting - Manually instrumented):**
    *   `vote`: Flask application for casting votes.
    *   `result`: Node.js application to display voting results.
    *   `worker`: .NET worker service to process votes (likely interacts with a database).
    *   `seed-data`:  Scripts/tools for populating initial data.
    *   `postgresdb`: Database for storing votes.
    *  `redis-cache`: Cache

**Observability Components:**

*   **OpenTelemetry Collector:** Receives, processes, and exports telemetry data.
*   **Zipkin:** Distributed tracing system (for `shopping-app` traces).
*   **Prometheus:** Time-series database for metrics (from all services).
*   **Grafana:** Visualization tool for metrics, traces, and logs.
*   **Loki:** Log aggregation system (for `shopping-app` logs).
*   **Azure Monitor:** (Optional) Cloud monitoring (for `voting-app` telemetry).
* **Jaeger:** all-in-one

**Data Flow:**

1.  User interacts with the `shopping-app` `frontend` or the `voting-app` `vote` service.
2.  Application services (auto or manually instrumented) generate telemetry data (traces, metrics, logs).
3.  This data is sent to the OpenTelemetry Collector via the OTLP protocol.
4.  The OpenTelemetry Collector processes the data (batching, filtering).
5.  The Collector exports:
    *   `shopping-app` traces to Zipkin.
    *   All metrics to Prometheus.
    *  `shopping-app` logs to Loki.
    *   `voting-app` traces, metrics, and logs to Azure Monitor.
    *   All data to a `debug` exporter (for troubleshooting - remove in production).
6.  Grafana visualizes data from Prometheus, Zipkin and Loki.

## 3. Prerequisites

*   **Azure Subscription:** For AKS.
*   **Azure CLI:**  Installed and configured (`az login`).
*   **kubectl:** Kubernetes command-line tool.
*   **Docker:** Docker Desktop or another Docker engine.
*   **Python 3.9+:** For the `shopping-app` and `voting-app` (vote service)
* **Node.js and npm:** For `voting-app` (result service).
* **.NET SDK:** For `voting-app` (worker service)
*   **A Container Registry:** Docker Hub, Azure Container Registry (ACR), etc.
*   **(Optional) Terraform:** If using Terraform for infrastructure provisioning.
*   **(Optional) Ansible:** If using Ansible for configuration management.
*   **(Optional) Helm:** If using Helm charts for Grafana/Prometheus/Loki/etc.
* **(Optional) Application Insights:** To use Azure monitor.

## 4. Setup and Installation

### 4.1. Clone the Repository

```bash
git clone <your-repository-url>
cd <your-repository-directory>
```

### 4.2. Docker Hub Credentials and Login

Before building and pushing the Docker images, you need to log in to Docker Hub using your credentials.

Create a Docker Hub Account (if you don't have one): Go to https://hub.docker.com/ and create a free account.

Docker Login: Open a terminal and run the following command, replacing <your-dockerhub-username> with your actual Docker Hub username:

```bash
docker login -u <your-dockerhub-username>
```

### 4.3. Build Docker Images (with your Docker Hub username)

Now, build the Docker images for each service.  Important: Replace <your-dockerhub-username> with your actual Docker Hub username in all of the following docker build commands.  This ensures the images are tagged correctly for your Docker Hub repository.

```bash
# shopping-app
cd application/shopping-app
docker build -t <your-dockerhub-username>/frontend-service:v2 frontend/
docker build -t <your-dockerhub-username>/orders-service:v2 orders/
docker build -t <your-dockerhub-username>/payment-service:v2 payment/
docker build -t <your-dockerhub-username>/products-service:v2 products/
docker build -t <your-dockerhub-username>/recommendations-service:v2 recommendations/

# voting-app
cd ../voting-app
docker build -t <your-dockerhub-username>/voting-app-vote:v2 vote/
docker build -t <your-dockerhub-username>/voting-app-result:v2 result/
docker build -t <your-dockerhub-username>/voting-app-worker:v2 worker/

cd ../..  # Go back to project root
```


### 4.5. Deploying applications


Kubernetes (using kubectl) (Recommended for this demo): This is the most direct method and is suitable for learning and development. We'll provide detailed instructions for this method.

For simplicity and clarity, the following steps assume you are using kubectl directly.


