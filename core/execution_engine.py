
import pandas as pd
import numpy as np
import sys
import io
import traceback
import warnings
import json
import matplotlib
import base64
# Force non-interactive backend to prevent popups
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from typing import Any, Dict, Optional, Tuple

class CodeExecutor:
    """
    Executes Python code in a persistent state with a DataFrame loaded.
    Supports Matplotlib (Base64) and Plotly (JSON) visualizations.
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
            (success, result_variable, stdout_output, plot_data)
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
            
            # Check for plots
            plot_data = self._capture_plot()
            output = buffer.getvalue()
            
            return True, final_result, output, plot_data
            

        except Exception as e:
            # Capture traceback
            tb = traceback.format_exc()
            return False, None, tb
            
        finally:
            sys.stdout = original_stdout
            
            # Reset matplotlib backend if it was used (to avoid interfering with main thread)
            # This is a precaution for some environments
            pass

    def _capture_plot(self) -> Optional[Dict[str, Any]]:
        """
        Check if a plot was created and return it.
        Priority: Plotly 'fig' object > Matplotlib active figures.
        """
        try:
            # 1. Check for Plotly 'fig' variable
            if "fig" in self.globals:
                fig = self.globals["fig"]
                if hasattr(fig, "to_json"):
                     # It's likely a Plotly figure
                     json_str = fig.to_json()
                     return {"type": "plotly", "data": json_str}

            # 2. Check for Matplotlib figures
            if plt.get_fignums():
                buf = io.BytesIO()
                plt.savefig(buf, format='png', bbox_inches='tight', transparent=True)
                buf.seek(0)
                img_str = base64.b64encode(buf.read()).decode('utf-8')
                plt.close('all')
                return {"type": "image", "data": img_str}

        except Exception as e:
            # Fallback or log error
            pass
        return None

    def update_df(self, new_df: pd.DataFrame):
        """Update the dataframe in the execution context."""
        self.df = new_df
        self.globals["df"] = new_df

    def get_context_keys(self):
        """Debug helper to see what variables are in memory."""
        return list(self.globals.keys())
