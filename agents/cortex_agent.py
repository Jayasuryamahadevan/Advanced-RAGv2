
import logging
from typing import Dict, Any, Optional
import pandas as pd
from agents.agentic_base import BaseAgent, AgentContext, AgentResult, AgentRole
from core.execution_engine import CodeExecutor

logger = logging.getLogger(__name__)

class CortexAgent(BaseAgent):
    """
    The Brain of Genorai Cortex.
    Uses LLM to generate Python code for any data query.
    Replaces QueryAgent and DataAgent.
    """
    
    def __init__(self, context: AgentContext):
        super().__init__(name="CortexAgent", role=AgentRole.ANALYSIS)
        self.context = context
        self.executor = CodeExecutor(context.data)
        
        # Build schema string for LLM
        self.schema_info = self._get_schema_summary()

    def _get_schema_summary(self) -> str:
        """Create a dense summary of columns and types."""
        df = self.context.data
        summary = "Columns:\n"
        for col in df.columns:
            dtype = df[col].dtype
            sample = df[col].dropna().iloc[0] if not df[col].dropna().empty else "N/A"
            summary += f"- {col} ({dtype}): e.g., '{sample}'\n"
        return summary

    def think(self, input_data: str) -> Dict[str, Any]:
        """
        Analyze query and plan execution.
        """
        return {"query": input_data} # Direct execution model

    def act(self, plan: Dict[str, Any]) -> AgentResult:
        query = plan["query"]
        
        # 1. Generate Code using LLM
        code = self._generate_analysis_code(query)
        
        # 2. Execute Code (with automatic retry)
        success, result, output = self._execute_with_retry(query, code)
        
        # 3. Formulate Answer
        final_answer = self._synthesize_answer(query, code, result, output, success)
        
        return AgentResult(
            agent=self.name,
            action="cortex_execution",
            result=final_answer,
            confidence=1.0 if success else 0.0,
            metadata={"code": code, "output": output}
        )
        
    def _generate_analysis_code(self, query: str, error_context: str = "") -> str:
        """Prompt LLM to write pandas code."""
        prompt = f"""
You are an expert Python Data Scientist. 
You have a pandas DataFrame `df` loaded in memory.
User Query: "{query}"

Schema:
{self.schema_info}

Task: Write Python code to answer the query.
Rules:
1. Use `df` variable directly.
2. PRINT the final answer using `print()`.
3. If the answer is a DataFrame or List, print it clearly.
4. For aggregation, group by relevant columns.
5. Handle string matching case-insensitively (str.lower()).
6. NO markdown backticks. Just pure code.
7. Wrap in try-except if necessary, but keep it simple.
8. AVOID SettingWithCopyWarning: Use .copy() when filtering if you plan to modify.
9. Verify variable names before use. Don't use variables like 'filtered_DATE' unless defined.
10. Ensure column names are correct (check df.columns).
11. PREDICTION/FORECASTING: Use `sklearn`. One-hot encode categoricals if needed. Split X/y. Train on full data or split. Print the prediction or model score/coefficients clearly.

{error_context}

Code:
"""
        # Call LLM directly
        from agents.agentic_base import call_llm
        code = call_llm(prompt)
        return self._clean_code(code)

    def _execute_with_retry(self, query: str, initial_code: str) -> tuple:
        """Run code, if it fails, ask LLM to fix it."""
        code = initial_code
        
        for attempt in range(3):
            success, result, output = self.executor.execute_code(code)
            
            if success:
                return True, result, output
            
            # If failed, retry
            logger.warning(f"Attempt {attempt+1} failed: {output}")
            error_msg = f"Previous code failed with error:\n{output}\nFix the code."
            code = self._generate_analysis_code(query, error_context=error_msg)
            
        return False, None, "Execution failed after 3 attempts."

    def _clean_code(self, code: str) -> str:
        """Strip markdown ticks."""
        code = code.strip()
        if code.startswith("```python"):
            code = code[9:]
        elif code.startswith("```"):
            code = code[3:]
        if code.endswith("```"):
            code = code[:-3]
        return code.strip()

    def _synthesize_answer(self, query: str, code: str, result: Any, output: str, success: bool) -> str:
        """Convert raw output to nice text."""
        if not success:
            return f"I failed to analyze the data. Error:\n{output}"
            
        # Prioritize stdout, but fallback to result variable
        text_output = output.strip()
        if not text_output and result is not None:
            text_output = str(result)
            
        if not text_output:
            return "Analysis completed successfully, but no output was generated."

        # If output is short, return it directly
        if len(text_output) < 1000:
            return text_output
            
        return f"Analysis Result:\n{text_output[:1000]}..." # Truncate if huge
