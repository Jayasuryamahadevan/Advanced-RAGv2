
import pandas as pd
import numpy as np
import sys
import io
import traceback
import warnings
from typing import Any, Dict, Optional, Tuple

class CodeExecutor:
    """
    Executes Python code in a persistent state with a DataFrame loaded.
    Designed for local, safe execution of LLM-generated analysis code.
    """
    
    def __init__(self, df: pd.DataFrame):
        self.df = df
        # Prepare valid global context (pandas, numpy, and the dataframe)
        self.globals = {
            "pd": pd,
            "np": np,
            "df": df,
            "result": None # Placeholder for output
        }
        # Suppress common pandas warnings to keep UI clean
        warnings.filterwarnings('ignore', category=pd.errors.SettingWithCopyWarning)
        warnings.filterwarnings('ignore', category=UserWarning)
    
    def execute_code(self, code: str) -> Tuple[bool, Any, str]:
        """
        Execute python code block.
        
        Args:
            code (str): The python code to run. Expected to print output or assign to 'result'.
            
        Returns:
            (success, result_variable, stdout_output)
        """
        
        # Buffer to capture stdout
        buffer = io.StringIO()
        original_stdout = sys.stdout
        sys.stdout = buffer
        
        try:
            # Dangerous imports check (Basic sandbox)
            if "os.system" in code or "subprocess" in code or "sys.exit" in code:
                raise ValueError("Security Violation: Forbidden OS commands detected.")
            
            # Execute code in strict global scope
            exec(code, self.globals)
            
            # Check if 'result' variable matches our expectation
            final_result = self.globals.get("result", None)
            
            output = buffer.getvalue()
            return True, final_result, output
            
        except Exception as e:
            # Capture traceback
            tb = traceback.format_exc()
            return False, None, tb
            
        finally:
            sys.stdout = original_stdout

    def update_df(self, new_df: pd.DataFrame):
        """Update the dataframe in the execution context."""
        self.df = new_df
        self.globals["df"] = new_df

    def get_context_keys(self):
        """Debug helper to see what variables are in memory."""
        return list(self.globals.keys())
