# E-Commerce Microservices with OpenTelemetry

This repository contains a demo e-commerce application built with multiple microservices, instrumented with OpenTelemetry for observability, and designed for deployment to Kubernetes (specifically, Azure Kubernetes Service - AKS).

## Table of Contents

1.  [Project Overview](#project-overview)
2.  [Architecture](#architecture)
3.  [Prerequisites](#prerequisites)
4.  [Setup and Installation](#setup-and-installation)
    *   [Clone the Repository](#clone-the-repository)
    *   [Install Dependencies](#install-dependencies)
    *   [Build Docker Images](#build-docker-images)
    *   [Push Docker Images](#push-docker-images)
    *   [Create Kubernetes Namespace](#create-kubernetes-namespace)
    *   [Create Secrets (Optional but Recommended)](#create-secrets-optional-but-recommended)
    *   [Deploy to Kubernetes](#deploy-to-kubernetes)
5.  [Verification and Testing](#verification-and-testing)
    *   [Check Pod Status](#check-pod-status)
    *   [Check Service Status](#check-service-status)
    *   [Access the Frontend](#access-the-frontend)
    *   [Place a Test Order](#place-a-test-order)
    *   [Access Zipkin](#access-zipkin)
    *   [Access Prometheus](#access-prometheus)
    *   [Access Grafana](#access-grafana)
6.  [Observability Details](#observability-details)
    *   [OpenTelemetry Configuration](#opentelemetry-configuration)
    *   [Collector Configuration](#collector-configuration)
    *   [Viewing Traces](#viewing-traces)
    *   [Viewing Metrics](#viewing-metrics)
    *   [Viewing Logs](#viewing-logs)
7.  [Troubleshooting](#troubleshooting)
8.  [Cleaning Up](#cleaning-up)
9.  [Directory Structure](#directory-structure)
10. [Contributing](#contributing)
11. [Observability Concepts](#observability-concepts)
    * [What is Observability?](#what-is-observability)
    * [OpenTelemetry (OTel)](#opentelemetry-otel)
    * [The OpenTelemetry Collector](#the-opentelemetry-collector)
    * [Observability Backends](#observability-backends)
    * [Demo Application and its setup](#demo-application-and-its-setup)
    * [Use Cases of OpenTelemetry](#use-cases-of-opentelemetry)
## 1. Project Overview

This project demonstrates a basic e-commerce application built using a microservices architecture.  It showcases how to instrument applications with OpenTelemetry to collect traces, metrics, and logs, and how to use popular open-source tools (Zipkin, Prometheus, Grafana, Loki) for observability.  The application is designed for deployment to Kubernetes.

## 2. Architecture

The application consists of the following microservices:

*   **`frontend-service`:** A Python Flask application that serves the web UI.  Users interact with this service to browse products and place orders.
*   **`orders-service`:** A Python Flask application that handles order placement. It interacts with the `products-service`, `recommendations-service`, and `payment-service`.
*   **`products-service`:** A Python Flask application that provides product information.
*   **`recommendations-service`:** A Python Flask application that generates product recommendations.
*   **`payment-service`:** A Python Flask application that simulates payment processing.
*   **`voting-app`:**  A separate application (not part of the core e-commerce flow) used to demonstrate routing telemetry to Azure Monitor.  (You'll need to create this if you want to test the Azure Monitor integration).

Observability Components:

*   **OpenTelemetry Collector:**  A central component that receives, processes, and exports telemetry data.
*   **Zipkin:**  A distributed tracing system used to visualize traces from the e-commerce application.
*   **Prometheus:**  A time-series database used to store and query metrics.
*   **Grafana:**  A visualization tool used to create dashboards for metrics (from Prometheus) and traces (from Zipkin).
*   **Loki:** Log aggregation system.
*   **Azure Monitor:** (Optional) Microsoft's cloud-based monitoring service.  Used for the `voting-app` telemetry.

## 3. Prerequisites

*   **An Azure Subscription:** You'll need an Azure subscription to use AKS.
*   **Azure CLI:** Install and configure the Azure CLI (`az`).  You'll need to be logged in (`az login`).
*   **kubectl:** Install `kubectl`, the Kubernetes command-line tool.
*   **Docker:** Install Docker Desktop or another Docker engine.
*   **Python 3.9+:** Required for building and running the application services.
*   **A Container Registry:** You'll need a container registry to store your Docker images.  Docker Hub is a good option for testing, but for production, consider Azure Container Registry (ACR) or another private registry.
* **(Optional) Helm:** If deploying Grafana/Prometheus/Loki via Helm, you'll need Helm installed.
* **(Optional) Application Insights:** To use Azure monitor, create Application Insights.

## 4. Setup and Installation

### 4.1. Clone the Repository

```bash
git clone <your-repository-url>
cd <your-repository-directory>

4.2. Install Dependencies

Each Python service has a requirements.txt file.  Install the dependencies for each service:

```bash
cd frontend-service
pip install -r requirements.txt
cd ../orders-service
pip install -r requirements.txt
# ... repeat for products-service, recommendations-service, payment-service ...
cd ..


