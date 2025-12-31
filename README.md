# Genorai Cortex (RAG v2)

This is the fully autonomous, LLM-powered Data Analysis Engine.

## Requirements
- Python 3.10+
- Dependencies:
  ```bash
  pip install pandas numpy rich scikit-learn requests loguru openpyxl
  ```
- Local LLM:
  - **Ollama** running on `http://127.0.0.1:11434`
  - Model: `deepseek-v3.1:671b-cloud` (Make sure it's pulled)

## How to Run

1. **Double-click** `run_genorai.bat`.
2. **Or run via terminal:**
   ```bash
   python agentic_interactive.py "sales.csv"
   ```

## Features
- **Dynamic Coding**: Writes Python code for any query.
- **Universal**: Works with any CSV/Excel file.
- **Predictive**: Supports forecasting queries like "Predict future revenue".
- **Self-Healing**: Auto-corrects 90% of code errors.

## 🐳 Quick Start with Docker (For Friends & Sharing)

The easiest way to share and run Genorai Cortex is using Docker. No Python setup required!

### 1. Requirements
- **Docker Desktop** installed.
- **Ollama** running locally (for the brain).

### 2. How to Run (One Command)
Your friend just needs to run:
```bash
git clone https://github.com/Jayasuryamahadevan/Advanced-RAGv2
cd Advanced-RAGv2/RAGv2
docker-compose up --build
```

The system will start automatically and connect to the host's Ollama.

### 3. Sharing a Pre-Built Image (Optional)
If you want to send them a direct Docker Link (so they don't need to build):
1. Create a repository on [Docker Hub](https://hub.docker.com/).
2. Run:
   ```bash
   docker login
   docker build -t your-username/genorai-cortex:v2 .
   docker push your-username/genorai-cortex:v2
   ```
3. Your friend can then run:
   ```bash
   docker run -it --add-host=host.docker.internal:host-gateway your-username/genorai-cortex:v2
   ```
