
import sys
import pandas as pd
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from agents.agentic_base import AgentContext
from agents.orchestrator import OrchestratorAgent
from core.execution_engine import CodeExecutor

def test_rag_v3_components():
    print(">>> Setting up Test Data...")
    # Create dummy data
    data = pd.DataFrame({
        'sales': [100, 200, 150, 400, 500, 100],
        'date': pd.date_range(start='2024-01-01', periods=6),
        'region': ['North', 'South', 'North', 'South', 'West', 'East']
    })
    
    print("\n>>> Initializing Orchestrator (Multi-Agent System)...")
    context = AgentContext(data)
    orchestrator = OrchestratorAgent(context)
    
    print(f"Agents initialized: {orchestrator.name}")
    print(f"Sub-agents: {orchestrator.coder.name}, {orchestrator.critic.name}")
    
    # Test Question
    query = "What is the total sales for the North region?"
    print(f"\n>>> Running Test Query: '{query}'")
    
    result = orchestrator.run(query)
    
    print("\n>>> Result Recieved:")
    print(f"Agent: {result.agent}")
    print(f"Action: {result.action}")
    print(f"Confidence: {result.confidence}")
    print(f"Result Output: {result.result}")
    
    assert result.confidence == 1.0
    assert "250" in str(result.result) or "250" in str(result.metadata.get('code')), "Answer should be 250 (100+150)"
    
    print("\n>>> Verification SUCCESS!")

if __name__ == "__main__":
    test_rag_v3_components()
