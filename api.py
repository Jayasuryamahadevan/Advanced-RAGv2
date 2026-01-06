import os
import sys
from pathlib import Path
from typing import Dict, Any, Optional, List
from threading import Lock

from fastapi import FastAPI, HTTPException, BackgroundTasks, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
from loguru import logger
import pandas as pd
import shutil
import os

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

from agents.agentic_base import AgentContext
from agents.orchestrator import OrchestratorAgent
from utils.data_loader import DataLoader
from config import settings

# -------------------------------------------------------------------------
# App Configuration
# -------------------------------------------------------------------------

app = FastAPI(
    title="Genorai Cortex API",
    description="Agentic RAG Engine v3.0 - Elite Tier",
    version="3.0.0"
)

# CORS Configuration
origins = [
    "http://localhost:3000",
    "http://localhost:5173",  # Default Vite port
    "http://127.0.0.1:3000",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------------------------------------------------
# Global State
# -------------------------------------------------------------------------

class AppState:
    def __init__(self):
        self.cortex: Optional[OrchestratorAgent] = None
        self.data: Optional[pd.DataFrame] = None
        self.lock = Lock()

state = AppState()

# -------------------------------------------------------------------------
# Models
# -------------------------------------------------------------------------

class InitRequest(BaseModel):
    file_path: Optional[str] = None
    
class AnalyzeRequest(BaseModel):
    query: str
    
class AgentResponse(BaseModel):
    result: str
    confidence: float
    metadata: Dict[str, Any] = {}
    time_taken: float

# -------------------------------------------------------------------------
# Startup / Shutdown
# -------------------------------------------------------------------------

@app.on_event("startup")
async def startup_event():
    """Initialize the system on startup."""
    logger.info("Genorai Cortex API starting up...")
    
    # Try to load default data if available (e.g., sales.csv)
    default_data = Path("sales.csv")
    if default_data.exists():
        try:
            loader = DataLoader()
            data = loader.load(str(default_data))
            context = AgentContext(data)
            state.data = data
            state.cortex = OrchestratorAgent(context)
            logger.info(f"Loaded default dataset: {default_data}")
        except Exception as e:
            logger.error(f"Failed to load default data: {e}")

# -------------------------------------------------------------------------
# Endpoints
# -------------------------------------------------------------------------

@app.get("/health")
async def health_check():
    return {
        "status": "online",
        "version": "3.0.0",
        "agent_ready": state.cortex is not None
    }

@app.post("/api/analyze", response_model=AgentResponse)
async def analyze_data(request: AnalyzeRequest):
    """
    Main endpoint for user queries.
    """
    if not state.cortex:
        raise HTTPException(status_code=400, detail="System not initialized with data.")
    
    try:
        import time
        start_time = time.time()
        
        # Run the agent
        # The existing run method is synchronous, so we might block the event loop.
        # For a production app, we should run this in a threadpool.
        response = state.cortex.run(request.query)
        
        elapsed = time.time() - start_time
        
        return AgentResponse(
            result=str(response.result),
            confidence=response.confidence,
            metadata=response.metadata or {},
            time_taken=elapsed
        )
        
    except Exception as e:
        logger.error(f"Analysis failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/load-data")
async def load_data(request: InitRequest):
    """
    Load a specific dataset.
    """
    path_str = request.file_path or "sales.csv"
    path = Path(path_str)
    
    if not path.exists():
        # Try full path if relative fails
        if not path.is_absolute():
             # maybe it's just a filename in the root
             path = Path(__file__).parent / path_str
             
    if not path.exists():
        raise HTTPException(status_code=404, detail=f"File not found: {path_str}")
        
    try:
        with state.lock:
            loader = DataLoader()
            data = loader.load(str(path))
            context = AgentContext(data)
            state.data = data
            state.cortex = OrchestratorAgent(context)
            
        return {
            "status": "success",
            "message": f"Loaded {path.name}",
            "rows": len(data),
            "columns": list(data.columns)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to load data: {e}")

@app.post("/api/upload")
async def upload_file(file: UploadFile = File(...)):
    """
    Upload a file and load it into the system.
    """
    try:
        # Create uploads directory if not exists
        upload_dir = Path("uploads")
        upload_dir.mkdir(exist_ok=True)
        
        file_path = upload_dir / file.filename
        
        # Save file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        # Load data
        with state.lock:
            loader = DataLoader()
            data = loader.load(str(file_path))
            context = AgentContext(data)
            state.data = data
            state.cortex = OrchestratorAgent(context)
            
        logger.info(f"Uploaded and loaded: {file.filename}")
        
        return {
            "status": "success",
            "message": f"Successfully loaded {file.filename}",
            "filename": file.filename,
            "rows": len(data),
            "columns": list(data.columns)
        }
        
    except Exception as e:
        logger.error(f"Upload failed: {e}")
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)
