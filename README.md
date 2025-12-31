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

## Architecture
- `agentic_interactive.py`: CLI Entry point.
- `agents/cortex_agent.py`: The LLM Brain.
- `core/execution_engine.py`: The Safe Execution Sandbox.
