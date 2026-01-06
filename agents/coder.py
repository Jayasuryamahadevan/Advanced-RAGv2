
import logging
import pandas as pd
from typing import Dict, Any, Optional
from agents.agentic_base import BaseAgent, AgentRole, AgentResult, call_llm
from memory.vector_store import CodeMemory

logger = logging.getLogger(__name__)

class CoderAgent(BaseAgent):
    """
    Specialist Agent: Converts Natural Language -> Python Code.
    Uses RAG (Memory) to recall past solutions.
    """
    
    def __init__(self, context_data: pd.DataFrame, memory: CodeMemory = None):
        super().__init__(name="CoderAgent", role=AgentRole.ANALYSIS)
        self.data_schema = self._get_schema_summary(context_data)
        self.memory = memory

    def _get_schema_summary(self, df: pd.DataFrame) -> str:
        """Create a dense summary of columns and types."""
        summary = "Columns:\n"
        for col in df.columns:
            dtype = df[col].dtype
            sample = df[col].dropna().iloc[0] if not df[col].dropna().empty else "N/A"
            summary += f"- {col} ({dtype}): e.g., '{sample}'\n"
        return summary

    def think(self, input_data: str) -> Dict[str, Any]:
        """
        Input: User Query
        Output: Plan with 'code'
        """
        query = input_data
        
        # 1. RAG Step: Check Memory
        past_solution = ""
        if self.memory:
            memories = self.memory.recall(query)
            if memories:
                best = memories[0]
                if best['distance'] < 0.3: # Threshold for similarity
                    logger.info(f"Found relevant memory: {best['intent']}")
                    past_solution = f"\nHints from similar past problem ('{best['intent']}'):\n```python\n{best['code']}\n```\n"

        # 2. Generate Prompt
        # Strict Visualization Rules
        if "plot" in query.lower() or "visualize" in query.lower() or "chart" in query.lower() or "graph" in query.lower():
            prompt = f"""
You are an expert Python Data Scientist specializing in Interactive Visualizations.
User Query: "{query}"

Schema:
{self.data_schema}

{past_solution}

Task: Write Python code to create an INTERACTIVE Plotly visualization.

STRICT RULES For Visualization:
1. USE ONLY `plotly.express` (as px) or `plotly.graph_objects` (as go).
2. DO NOT use matplotlib or seaborn.
3. Assign the final plotly figure object to a variable named `fig`.
4. Set the template to "plotly_dark" or styled for a dark background.
5. Make the chart ELITE: Enable tooltips, use vibrant colors (cyan, purple), and legible fonts.
6. PRINT a brief textual summary of what the plot shows using `print()`.

Standard Rules:
1. Use `df` variable directly.
2. Handle string matching case-insensitively.
3. Ensure column names exist.
4. NO markdown backticks. Pure code only.

Code:
"""
        else:
            # Standard Analysis Prompt
            prompt = f"""
You are an expert Python Data Scientist. 
User Query: "{query}"

Schema:
{self.data_schema}

{past_solution}

Task: Write Python code to answer the query.
Rules:
1. Use `df` variable directly.
2. PRINT the final answer using `print()`.
3. If the answer is a DataFrame or List, print it clearly.
4. For aggregation, group by relevant columns.
5. Handle string matching case-insensitively (str.lower()).
6. NO markdown backticks. Just pure code.
7. Wrap in try-except block for robustness.
8. AVOID SettingWithCopyWarning.
9. Validate all variable names before usage.
10. Ensure column names exist in the DataFrame.

Code:
"""
        return {"prompt": prompt}

    def act(self, plan: Dict[str, Any]) -> AgentResult:
        prompt = plan["prompt"]
        code = call_llm(prompt)
        # Clean code
        code = code.strip().replace("```python", "").replace("```", "").strip()
        
        return AgentResult(
            agent=self.name,
            action="propagate_code",
            result=code,
            confidence=0.9
        )
