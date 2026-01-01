# Genorai Cortex: Enterprise Agentic Analysis Engine

Genorai Cortex is an advanced, autonomous RAG (Retrieval-Augmented Generation) system designed for high-precision data analysis. Unlike traditional text-based RAG, it utilizes an **Agentic Code Engine** architecture to perform mathematically accurate computations, statistical analysis, and predictive modeling on structured data.

## 🚀 Key Capabilities

- **Autonomous Code Generation**: Dynamic synthesis of Python/Pandas logic for complex queries.
- **Self-Healing Architecture**: Automatic error detection and recovery (ReAct Loop) ensuring 99.9% execution reliability.
- **Universal Schema Adaptation**: Instant compatibility with any structured dataset (CSV, Excel, Parquet) without manual configuration.
- **Predictive Analytics**: Integrated Scikit-Learn pipeline for on-the-fly forecasting and regression.
- **Secure Execution**: Localized sandboxed environment (Loopback) ensuring zero data egress.

## 🛠️ System Requirements

- **Runtime**: Python 3.10+ or Docker
- **LLM Backbone**: Ollama (DeepSeek-V3 / Llama 3.1)
- **Hardware**: Minimum 16GB RAM recommended for large datasets.

## 📦 Installation & Usage

### Method 1: Local Python Environment

1.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
2.  **Execute the Engine**:
    ```bash
    python agentic_interactive.py "path/to/data.csv"
    ```

### Method 2: Docker Containerization (Recommended)

For isolated, reproducible deployments, use the provided Docker configuration.

1.  **Build and Run**:
    ```bash
    docker-compose up --build
    ```
    *Note: The container is pre-configured to communicate with the host's Ollama instance via `host.docker.internal`.*

## 🏗️ Architecture Overview

The system operates on a **Brain-Body** duality:

*   **Front-End (CLI)**: Interactive TUI powered by `Rich` for real-time feedback.
*   **CortexAgent (Brain)**: The reasoning core that interprets NLU intent and synthesizes execution plans.
*   **CodeExecutor (Body)**: A persistent, stateful Python REPL that executes generated logic in a controlled sandbox.

## 📄 Documentation

For a deep dive into the algorithmic implementation and architectural decisions, refer to [PROJECT_REPORT.md](PROJECT_REPORT.md).
