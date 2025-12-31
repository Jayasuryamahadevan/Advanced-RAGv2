"""
Data loading utilities for industrial logs and sensor data.
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Optional, List, Dict, Any, Union
from datetime import datetime
from loguru import logger


class DataLoader:
    """
    Flexible data loader for industrial sensor/log data.
    Supports CSV, Parquet, and JSON formats.
    """
    
    SUPPORTED_FORMATS = [".csv", ".parquet", ".json", ".xlsx"]
    
    def __init__(self, data_dir: Optional[Path] = None):
        self.data_dir = data_dir or Path("D:/GenoraiRAG/data")
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self._loaded_datasets: Dict[str, pd.DataFrame] = {}
    
    def load(
        self,
        file_path: Union[str, Path],
        timestamp_col: Optional[str] = None,
        parse_dates: bool = True,
        **kwargs
    ) -> pd.DataFrame:
        """
        Load data from file with automatic format detection.
        
        Args:
            file_path: Path to data file
            timestamp_col: Column to use as datetime index
            parse_dates: Whether to parse date columns
            **kwargs: Additional arguments for pandas read functions
        
        Returns:
            Loaded DataFrame
        """
        path = Path(file_path)
        
        if not path.exists():
            # Check in data directory
            path = self.data_dir / file_path
            if not path.exists():
                raise FileNotFoundError(f"Data file not found: {file_path}")
        
        suffix = path.suffix.lower()
        
        logger.info(f"Loading data from {path} (format: {suffix})")
        
        if suffix == ".csv":
            df = pd.read_csv(path, **kwargs)
        elif suffix == ".parquet":
            df = pd.read_parquet(path, **kwargs)
        elif suffix == ".json":
            df = pd.read_json(path, **kwargs)
        elif suffix == ".xlsx":
            try:
                df = pd.read_excel(str(path), engine="openpyxl", **kwargs)
            except ImportError:
                 logger.error("Missing dependency 'openpyxl'. Please install: pip install openpyxl")
                 raise ImportError("To read Excel files, you need to install openpyxl: pip install openpyxl")
        elif suffix == ".xls":
             try:
                df = pd.read_excel(str(path), engine="xlrd", **kwargs)
             except Exception:
                 # It might be an HTML file saved as .xls (common in legacy systems)
                 try:
                     logger.warning("Failed with xlrd, trying as HTML table...")
                     dfs = pd.read_html(str(path), **kwargs)
                     if dfs:
                         df = dfs[0]
                     else:
                         raise ValueError("No tables found in file")
                 except ImportError:
                     raise ImportError("To read HTML-based .xls files, install lxml: pip install lxml")
                 except Exception as e:
                      # If both fail, raise the original xlrd error or a generic one
                      raise ValueError(f"Could not read .xls file. It refers to an unsupported format (XML/HTML?) or is corrupt. Error: {str(e)}")
        else:
            raise ValueError(f"Unsupported format: {suffix}")
        
        # Parse timestamps if specified
        if timestamp_col and timestamp_col in df.columns:
            df[timestamp_col] = pd.to_datetime(df[timestamp_col])
            df = df.sort_values(timestamp_col)
            df = df.set_index(timestamp_col)
            logger.info(f"Set {timestamp_col} as datetime index")
        elif parse_dates:
            # Auto-detect datetime columns
            df = self._auto_parse_dates(df)
        
        # Cache the dataset
        self._loaded_datasets[str(path)] = df
        
        logger.info(f"Loaded {len(df)} rows, {len(df.columns)} columns")
        return df
    
    def _auto_parse_dates(self, df: pd.DataFrame) -> pd.DataFrame:
        """Attempt to auto-detect and parse datetime columns."""
        date_keywords = ["time", "date", "timestamp", "datetime", "created", "updated"]
        
        for col in df.columns:
            col_lower = col.lower()
            if any(kw in col_lower for kw in date_keywords):
                try:
                    df[col] = pd.to_datetime(df[col])
                    logger.debug(f"Parsed {col} as datetime")
                except Exception:
                    pass
        
        return df
    
    def get_numeric_columns(self, df: pd.DataFrame) -> List[str]:
        """Get list of numeric columns suitable for EDA."""
        return df.select_dtypes(include=[np.number]).columns.tolist()
    
    def get_categorical_columns(self, df: pd.DataFrame) -> List[str]:
        """Get list of categorical columns."""
        return df.select_dtypes(include=["object", "category"]).columns.tolist()
    
    def get_datetime_columns(self, df: pd.DataFrame) -> List[str]:
        """Get list of datetime columns."""
        return df.select_dtypes(include=["datetime64"]).columns.tolist()
    
    def detect_machine_column(self, df: pd.DataFrame) -> Optional[str]:
        """
        Auto-detect the machine/equipment identifier column.
        Common patterns: machine_id, equipment_id, loom_id, asset_id, etc.
        """
        machine_keywords = [
            "machine", "equipment", "asset", "device", "loom", 
            "unit", "station", "robot", "sensor_id"
        ]
        
        for col in df.columns:
            col_lower = col.lower()
            if any(kw in col_lower for kw in machine_keywords):
                # Verify it's a categorical-like column
                if df[col].dtype == "object" or df[col].nunique() < 100:
                    logger.info(f"Detected machine column: {col}")
                    return col
        
        return None
    
    def split_by_machine(
        self, 
        df: pd.DataFrame, 
        machine_col: Optional[str] = None
    ) -> Dict[str, pd.DataFrame]:
        """
        Split DataFrame by machine/equipment for per-machine analysis.
        """
        if machine_col is None:
            machine_col = self.detect_machine_column(df)
        
        if machine_col is None:
            logger.warning("No machine column detected, returning single group")
            return {"all": df}
        
        machines = {}
        for machine_id in df[machine_col].unique():
            machines[str(machine_id)] = df[df[machine_col] == machine_id].copy()
        
        logger.info(f"Split data into {len(machines)} machine groups")
        return machines
    
    def get_data_summary(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Get a quick summary of the dataset."""
        return {
            "rows": len(df),
            "columns": len(df.columns),
            "numeric_cols": len(self.get_numeric_columns(df)),
            "categorical_cols": len(self.get_categorical_columns(df)),
            "datetime_cols": len(self.get_datetime_columns(df)),
            "memory_mb": df.memory_usage(deep=True).sum() / 1024 / 1024,
            "has_index": df.index.name is not None,
            "index_type": str(type(df.index).__name__),
            "date_range": self._get_date_range(df)
        }
    
    def _get_date_range(self, df: pd.DataFrame) -> Optional[Dict[str, str]]:
        """Get date range if datetime index exists."""
        if isinstance(df.index, pd.DatetimeIndex):
            return {
                "start": str(df.index.min()),
                "end": str(df.index.max()),
                "duration": str(df.index.max() - df.index.min())
            }
        return None


def generate_synthetic_industrial_data(
    n_samples: int = 10000,
    n_machines: int = 5,
    seed: int = 42
) -> pd.DataFrame:
    """
    Generate synthetic industrial sensor data for testing.
    Includes realistic patterns: trends, seasonality, outliers, missing values.
    """
    np.random.seed(seed)
    
    # Time range
    start_date = datetime(2024, 1, 1)
    timestamps = pd.date_range(start=start_date, periods=n_samples, freq="5min")
    
    # Machine IDs
    machines = [f"Machine_{i:02d}" for i in range(1, n_machines + 1)]
    machine_ids = np.random.choice(machines, n_samples)
    
    # Base sensor readings with machine-specific offsets
    machine_offsets = {m: np.random.uniform(-5, 5) for m in machines}
    
    # Temperature sensor (with trend and seasonality)
    hour_of_day = timestamps.hour
    day_effect = np.sin(2 * np.pi * hour_of_day / 24) * 5  # Daily pattern
    trend = np.linspace(0, 3, n_samples)  # Slight upward trend
    noise = np.random.normal(0, 2, n_samples)
    temperature = 65 + day_effect + trend + noise
    temperature += np.array([machine_offsets[m] for m in machine_ids])
    
    # Vibration sensor (with some correlation to temperature)
    vibration = 0.3 * temperature + np.random.normal(0, 1.5, n_samples)
    
    # Pressure sensor
    pressure = 100 + np.random.normal(0, 5, n_samples)
    
    # RPM (with shift patterns)
    shift = np.where(hour_of_day < 8, 0, np.where(hour_of_day < 16, 1, 2))
    rpm_base = np.where(shift == 0, 1200, np.where(shift == 1, 1500, 1350))
    rpm = rpm_base + np.random.normal(0, 50, n_samples)
    
    # Warning count (correlated with high temperature)
    warning_prob = np.clip((temperature - 70) / 30, 0, 0.5)
    warning_count = np.random.binomial(5, warning_prob)
    
    # Status (mostly running, some maintenance)
    status = np.random.choice(
        ["RUNNING", "IDLE", "MAINTENANCE"], 
        n_samples, 
        p=[0.85, 0.10, 0.05]
    )
    
    # Create DataFrame
    df = pd.DataFrame({
        "timestamp": timestamps,
        "machine_id": machine_ids,
        "temperature": temperature,
        "vibration": vibration,
        "pressure": pressure,
        "rpm": rpm,
        "warning_count": warning_count,
        "status": status,
        "shift": shift
    })
    
    # Add outliers (2% of data)
    outlier_mask = np.random.random(n_samples) < 0.02
    df.loc[outlier_mask, "temperature"] += np.random.choice([-20, 25], outlier_mask.sum())
    df.loc[outlier_mask, "vibration"] *= 2.5
    
    # Add missing values (realistic patterns)
    # Sensor dropout (bursty)
    dropout_start = np.random.choice(n_samples - 50, 10)
    for start in dropout_start:
        gap_length = np.random.randint(5, 20)
        df.loc[start:start + gap_length, "vibration"] = np.nan
    
    # Random missing (MCAR)
    mcar_mask = np.random.random(n_samples) < 0.03
    df.loc[mcar_mask, "pressure"] = np.nan
    
    # Missing during maintenance (MNAR)
    maintenance_mask = df["status"] == "MAINTENANCE"
    df.loc[maintenance_mask, ["temperature", "vibration", "rpm"]] = np.nan
    
    df = df.set_index("timestamp")
    
    logger.info(f"Generated synthetic data: {len(df)} samples, {n_machines} machines")
    return df
