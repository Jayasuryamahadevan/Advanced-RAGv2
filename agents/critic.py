
import logging
from typing import Dict, Any
from agents.agentic_base import BaseAgent, AgentRole, AgentResult

logger = logging.getLogger(__name__)

class CriticAgent(BaseAgent):
    """
    Specialist Agent: Reviews Python Code for Security and Logic.
    """
    
    def __init__(self):
        super().__init__(name="CriticAgent", role=AgentRole.ANALYSIS)

    def think(self, input_data: str) -> Dict[str, Any]:
        """
        Input: Python Code
        Output: Verification Result
        """
        code = input_data
        issues = []
        
        # 1. Security Check (Simple regex-like)
        forbidden = ["os.system", "subprocess", "shutil", "sys.exit", "rm -rf"]
        for term in forbidden:
            if term in code:
                issues.append(f"Security Risk: Found forbidden term '{term}'")

        # 2. Logic Check (Heuristics)
        # 2. Logic Check (Heuristics)
        has_print = "print(" in code
        has_plot = "fig =" in code or "fig=" in code or "plt." in code
        
        if not has_print and not has_plot:
            issues.append("Logic Error: Code does not print output or generate a chart.")
        
        # 'df' check is too strict for generic questions (e.g. "what is 2+2"), removing blocker.
        # if "df" not in code:
        #      issues.append("Logic Error: Code does not appear to use the dataframe `df`.")

        return {
            "is_safe": len(issues) == 0,
            "issues": issues,
            "code": code
        }

    def act(self, plan: Dict[str, Any]) -> AgentResult:
        if plan["is_safe"]:
            return AgentResult(
                agent=self.name,
                action="approve_code",
                result="APPROVED",
                confidence=1.0
            )
        else:
            return AgentResult(
                agent=self.name,
                action="reject_code",
                result=f"REJECTED: {'; '.join(plan['issues'])}",
                confidence=0.0
            )
