"""
Agentic Framework - Base Agent and Tool Classes

A lightweight agentic framework for data Q&A.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional, Callable
from enum import Enum
from typing import Dict, Any, List, Optional, Callable
from enum import Enum
import pandas as pd
import requests
import json
from loguru import logger

def call_llm(prompt: str, model: str = "deepseek-v3.1:671b-cloud", timeout: int = 120) -> str:
    """Helper to call Ollama LLM."""
    try:
        url = "http://127.0.0.1:11434/api/generate"
        payload = {
            "model": model,
            "prompt": prompt,
            "stream": False,
            "options": {"temperature": 0.0} # Deterministic for code
        }
        response = requests.post(url, json=payload, timeout=timeout)
        response.raise_for_status()
        return response.json().get("response", "")
    except Exception as e:
        logger.error(f"LLM Call Failed: {e}")
        # Fallback to smaller model if timeouts
        if model != "llama3.1":
             logger.info("Retrying with llama3.1...")
             return call_llm(prompt, model="llama3.1")
        return ""



class AgentRole(Enum):
    """Agent roles in the system."""
    ORCHESTRATOR = "orchestrator"
    QUERY = "query"
    DATA = "data"
    ANALYSIS = "analysis"
    ANSWER = "answer"


@dataclass
class Tool:
    """A tool that an agent can use."""
    name: str
    description: str
    func: Callable
    parameters: List[str] = field(default_factory=list)
    
    def execute(self, **kwargs) -> Any:
        """Execute the tool with given parameters."""
        return self.func(**kwargs)


@dataclass
class AgentMessage:
    """Message passed between agents."""
    sender: str
    content: Any
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AgentResult:
    """Result from an agent's action."""
    agent: str
    action: str
    result: Any
    confidence: float = 1.0
    metadata: Dict[str, Any] = field(default_factory=dict)


class BaseAgent(ABC):
    """
    Base class for all agents.
    
    Each agent has:
    - A role (query, data, analysis, answer)
    - A set of tools it can use
    - A think() method for reasoning
    - An act() method for taking action
    """
    
    def __init__(self, name: str, role: AgentRole):
        self.name = name
        self.role = role
        self.tools: Dict[str, Tool] = {}
        self.memory: List[AgentMessage] = []
    
    def register_tool(self, tool: Tool):
        """Register a tool for this agent."""
        self.tools[tool.name] = tool
        logger.debug(f"[{self.name}] Registered tool: {tool.name}")
    
    def use_tool(self, tool_name: str, **kwargs) -> Any:
        """Use a registered tool."""
        if tool_name not in self.tools:
            raise ValueError(f"Tool '{tool_name}' not found")
        return self.tools[tool_name].execute(**kwargs)
    
    def remember(self, message: AgentMessage):
        """Store a message in memory."""
        self.memory.append(message)
    
    @abstractmethod
    def think(self, input_data: Any) -> Dict[str, Any]:
        """
        Reasoning step - analyze input and decide what to do.
        Returns a plan of action.
        """
        pass
    
    @abstractmethod
    def act(self, plan: Dict[str, Any]) -> AgentResult:
        """
        Action step - execute the plan and return result.
        """
        pass
    
    def run(self, input_data: Any) -> AgentResult:
        """
        Main execution: think -> act.
        """
        logger.info(f"[{self.name}] Processing input...")
        plan = self.think(input_data)
        result = self.act(plan)
        logger.info(f"[{self.name}] Completed with confidence {result.confidence}")
        return result


class AgentContext:
    """
    Shared context between agents.
    Contains the data and state that all agents can access.
    """
    
    def __init__(self, data: pd.DataFrame):
        self.data = data
        self.columns = list(data.columns)
        self.numeric_cols = data.select_dtypes(include=['number']).columns.tolist()
        self.categorical_cols = data.select_dtypes(include=['object', 'category']).columns.tolist()
        self.row_count = len(data)
        self.col_count = len(data.columns)
        
        # Detect ID columns - broadened for general datasets
        self.id_cols = [c for c in self.columns 
                       if any(x in c.lower() for x in ['id', 'code', 'key', 'serial', 'udi', 'number', 'name', 'sku', 'isbn'])]
        
        # If no explicit ID column, and first column is unique, use it
        if not self.id_cols and self.data[self.columns[0]].is_unique:
            self.id_cols = [self.columns[0]]
        
        # Detect target/key metrics columns
        self.target_cols = [c for c in self.columns 
                           if any(x in c.lower() for x in ['fail', 'target', 'label', 'class', 'status', 'output', 'price', 'total', 'rating', 'score'])]
        
        # Pre-compute stats
        self.stats = self._compute_stats()
        
        # Pre-compute correlations
        if len(self.numeric_cols) >= 2:
            self.correlations = data[self.numeric_cols].corr()
        else:
            self.correlations = None
            
        # Build Semantic Value Map: normalized_value -> [columns]
        self.value_to_cols = self._build_value_map()
        
    def _build_value_map(self) -> Dict[str, List[str]]:
        """
        Build a semantic map of {normalized_value: [columns]}.
        Used for NLU to map 'orange juice' -> 'product_name'.
        Values and Column Name tokens are mapped.
        """
        value_map = {}
        
        # Helper to add token
        def add_token(token, col):
            if len(token) > 2 and token not in ["the", "and", "for", "with", "from", "inc", "ltd"]:
                 if token not in value_map: value_map[token] = []
                 if col not in value_map[token]: value_map[token].append(col)

        # 1. Map Column Names (Numeric + Categorical)
        # This ensures 'amount' maps to 'AMOUNT' column etc.
        all_cols = self.categorical_cols + self.numeric_cols
        for col in all_cols:
             col_name_tokens = col.lower().replace('_', ' ').split()
             for token in col_name_tokens:
                 add_token(token, col)

        # 2. Map Categorical Values
        for col in self.categorical_cols:
            try:
                unique_vals = self.data[col].unique()
                if len(unique_vals) > 1000:  # Skip high cardinality ID-like columns
                    continue
                    
                for val in unique_vals:
                    if pd.isna(val):
                        continue
                        
                    # Normalize: string, strip, lower
                    val_str = str(val).strip().lower()
                    if not val_str:
                        continue
                        
                    # Full value map
                    if val_str not in value_map:
                        value_map[val_str] = []
                    if col not in value_map[val_str]:
                        value_map[val_str].append(col)
                    
                    # Also map tokens (words) to the column for fuzzy finding
                    # e.g. "Toll Plaza" -> map "toll", "plaza"
                    tokens = val_str.split()
                    for token in tokens:
                        add_token(token, col)
                        
            except Exception as e:
                logger.warning(f"Error building value map for column {col}: {e}")
                continue
                
        return value_map
    
    def _compute_stats(self) -> Dict[str, Dict]:
        """Compute statistics for all numeric columns."""
        stats = {}
        for col in self.numeric_cols:
            stats[col] = {
                "min": float(self.data[col].min()),
                "max": float(self.data[col].max()),
                "mean": float(self.data[col].mean()),
                "median": float(self.data[col].median()),
                "std": float(self.data[col].std()),
            }
        return stats
    
    def get_row(self, idx: int) -> pd.Series:
        """Get a specific row."""
        return self.data.loc[idx]
    
    def get_id(self, row: pd.Series) -> str:
        """Get the ID string for a row."""
        for col in self.id_cols:
            val = row.get(col)
            if pd.notna(val):
                return f"{col}={val}"
        return f"Row {row.name}"
