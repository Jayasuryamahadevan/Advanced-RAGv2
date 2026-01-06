
import logging
from typing import Dict, Any, Optional
import pandas as pd
from agents.agentic_base import BaseAgent, AgentContext, AgentResult, AgentRole
from agents.coder import CoderAgent
from agents.critic import CriticAgent
from core.execution_engine import CodeExecutor
from memory.vector_store import CodeMemory

logger = logging.getLogger(__name__)

class OrchestratorAgent(BaseAgent):
    """
    The Council Leader.
    Coordinates: Coder -> Critic -> Executor -> User.
    """
    
    def __init__(self, context: AgentContext):
        self.context = context # Keeps the data
        super().__init__(name="Orchestrator", role=AgentRole.ORCHESTRATOR)
        
        # Initialize Sub-Agents
        # Temporarily disabled ChromaDB for demo speed
        self.memory = None
        if False: # Disabled for demo
            try:
                self.memory = CodeMemory()
            except Exception:
                logger.warning("Could not initialize ChromaDB. Running without memory.")
                self.memory = None

        self.coder = CoderAgent(context.data, self.memory)
        self.critic = CriticAgent()
        self.executor = CodeExecutor(context.data)

    def think(self, input_data: str) -> Dict[str, Any]:
        """
        Input: User Query
        Plan: Determine delegation flow.
        """
        return {"query": input_data}

    def act(self, plan: Dict[str, Any]) -> AgentResult:
        query = plan["query"]
        logger.info(f"Orchestrating query: {query}")
        
        # 1. Ask Coder
        coder_result = self.coder.run(query)
        code = coder_result.result
        
        # 2. Ask Critic
        critic_result = self.critic.run(code)
        if "REJECTED" in str(critic_result.result):
             return AgentResult(
                 agent=self.name, 
                 action="error", 
                 result=f"Code check failed: {critic_result.result}",
                 confidence=0.0
             )
        
        # 3. Execute
        success, result, output, plot_data = self._execute_with_retry(query, code)
        
        # 4. Save to Memory if valid
        if success and self.memory:
            self.memory.save_context(query, code)

        # 5. Formulate Answer
        final_answer = self._synthesize_answer(output, success)
        
        metadata = {"code": code}
        if plot_data:
            metadata["plot"] = plot_data
        
        return AgentResult(
            agent=self.name,
            action="final_answer",
            result=final_answer,
            confidence=1.0 if success else 0.0,
            metadata=metadata
        )
    
    def _execute_with_retry(self, query: str, initial_code: str) -> tuple:
        """Run code, if it fails, ask LLM to fix it."""
        code = initial_code
        
        for attempt in range(3):
            # unpack 4 values now
            try:
                success, result, output, plot_data = self.executor.execute_code(code)
            except ValueError:
                # Fallback
                success, result, output = self.executor.execute_code(code)
                plot_data = None
            
            if success:
                return True, result, output, plot_data
            
            # If failed, retry (Ask Coder again with error context)
            logger.warning(f"Attempt {attempt+1} failed: {output}")
            
            # Re-prompt Coder
            retry_prompt = f"{query}\n\nFIX THIS ERROR:\n{output}"
            code = self.coder.run(retry_prompt).result
            
        return False, None, "Execution failed after 3 attempts.", None

    def _synthesize_answer(self, output: str, success: bool) -> str:
        if not success:
            return f"I failed to analyze the data. Error:\n{output}"
        
        text_output = output.strip()
        if len(text_output) < 2000:
            return text_output
        return f"Result:\n{text_output[:2000]}..."
