# Genorai Cortex V3.0 - Elite Tier Analytics 💎

> **State-of-the-Art RAG System with Interactive Visualization and Agentic Intelligence.**

Genorai Cortex V3 is an advanced Retrieval-Augmented Generation (RAG) platform designed for high-end data analytics. It combines a powerful **FastAPI Backend** with a **Premium React Frontend**, featuring agentic code execution and interactive **Plotly** visualizations.

## 🚀 Key Features

### 1. Elite "Chart-First" Dashboard
-   **Immersive Visualization**: The interface is designed to showcase data. Large, interactive charts take center stage.
-   **Interactive Engine**: Powered by **Plotly**, allowing users to zoom, pan, and hover over data points for granular insights.
-   **Glassmorphism UI**: A stunning dark-themed interface with subtle gradients, blurs, and premium typography (Outfit/Inter).

### 2. Agentic Intelligence
-   **Orchestrator Agent**: Manages the flow of information between specialized agents.
-   **Coder Agent (Elite)**: Strictly enforced to generate high-quality Python code for data analysis and **Plotly** visualizations using `pandas` and `plotly.express`.
-   **Critic Agent**: Reviews code for security (sandboxing) and logic errors before execution.

### 3. Smart Workflows
-   **Chart Selector**: Explicitly choose your visualization style (Bar, Line, Pie, Scatter, Heatmap, etc.) via a seamless overlay.
-   **Context-Aware Chat**: Discuss your data naturally. The AI understands the context of the uploaded file.
-   **Instant Analysis**: Upload a CSV, and the system automatically profiles rows, columns, and data quality.

## 🛠️ Tech Stack

### Frontend
-   **Framework**: React (Vite)
-   **Styling**: TailwindCSS, Framer Motion
-   **Visualization**: `react-plotly.js`, `lucide-react` icons
-   **font**: Google Fonts (Outfit, Inter)

### Backend
-   **API**: FastAPI (Uvicorn)
-   **Data Processing**: Pandas, NumPy
-   **AI Logic**: Custom Agentic Framework (Orchestrator, Coder, Critic)
-   **Plotting**: Plotly Graph Objects (JSON serialization)

## 📦 Installation & Setup

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/Jayasuryamahadevan/Advanced-RAGv2.git
    cd Advanced-RAGv2
    ```

2.  **Backend Setup**
    ```bash
    # Create virtual env (optional)
    python -m venv venv
    .\venv\Scripts\activate

    # Install dependencies
    pip install -r requirements.txt

    # Run Server
    python api.py
    ```
    *Server runs on `http://127.0.0.1:8000`*

3.  **Frontend Setup**
    ```bash
    cd frontend
    npm install
    npm run dev
    ```
    *Client runs on `http://localhost:5173`*

## 💡 How to Use

1.  **Upload**: Drag & drop your dataset (CSV/Excel) onto the landing page.
2.  **Analyze**:
    -   *Natural Language*: "Show me the trend of sales over time."
    -   *Explicit Charting*: Type "Visualize...", pick "Area Chart" from the menu, and watch it generate.
3.  **Interact**: Hover over the generated charts to see exact values.

---

**Developed by Jayasurya Mahadevan** | *Genorai Cortex - Redefining AI Analytics*
