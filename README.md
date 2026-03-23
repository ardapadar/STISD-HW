AI Intelligent Note Pro - Ultra Dashboard
AI Intelligent Note Pro is a cutting-edge, microservice-based ecosystem designed to transform traditional note-taking into a cognitive behavioral analysis tool. The platform utilizes a deterministic AI engine to evaluate user thought patterns and provide real-time cognitive insights.

 Project Overview
This project implements a high-performance microservice stack, orchestrated with Docker, secured with JWT, and automated via a robust CI/CD pipeline. It features a "Cognitive Intelligence Dashboard" that analyzes user data to determine brain dominance and memory metrics.

 Key Features
Cognitive AI Engine: Analyzes user inputs to calculate Retention, Detail, and Speed scores.

Brain Dominance Analysis: Visualizes "Left-Brained" vs "Right-Brained" tendencies using dynamic SVG filters.

Microservice Architecture: Decoupled services for Auth, Note Management, and Notifications.

Asynchronous Communication: Inter-service communication via HTTPX for high-efficiency email delivery.

Pro Dashboard UI: A modern, glassmorphic interface built with Chart.js and Plus Jakarta Sans.

 Technical Architecture and Infrastructure
The system follows a Clean Architecture pattern, ensuring separation of concerns across multiple layers:

API Layer (FastAPI): Handles request routing, Pydantic validation, and authentication.

Core Logic (Service Layer): Executes business rules and the AI cognitive scoring algorithm.

Database Layer (SQLAlchemy): Manages persistent storage with PostgreSQL/SQLite.

Gateway (Nginx): Acts as a reverse proxy, orchestrating traffic between services.


1. Complete CI/CD Pipeline
We implemented a professional pipeline using GitHub Actions. Every "push" to the main branch triggers:

Environment Setup: Virtual environment and dependency installation.

Linting & Formatting: Code quality checks.

Automated Testing: Execution of the test suite.

Container Build: Verification of Docker images.

2. Automated Testing
The system includes automated unit tests that validate the AI Logic Engine and API Endpoints. This ensures that cognitive score calculations remain accurate through every update.

3. Container Orchestration
The entire stack is containerized using Docker. Deployment is managed via Docker Compose, ensuring a "cloud-like" environment where services are isolated, health-checked, and network-linked.

 Getting Started
Prerequisites
Docker & Docker Compose

Bash
docker-compose up --build
Access the Dashboard:
Open http://localhost/static/index.html in your browser.
<img width="1893" height="912" alt="image" src="https://github.com/user-attachments/assets/cfaf50b1-cdc2-4c1e-b8d1-1dab4a767240" />


docker-compose up --build
Access the Dashboard:
Open http://localhost/static/index.html in your browser.
