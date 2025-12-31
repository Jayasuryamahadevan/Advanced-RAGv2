"""
Configuration management for GenoraiRAG Agentic Analytics System.
"""

from pathlib import Path
from typing import Optional
from pydantic import BaseModel, Field
import os


class LLMConfig(BaseModel):
    """LLM configuration for agent reasoning."""
    # Primary model - will try in order until one works
    model_name: str = Field(default="deepseek-v3.1:671b-cloud", description="Primary Ollama model")
    # Fallback models in order of preference (local models available)
    fallback_models: list = Field(
        default=["qwen2.5:1.5b", "qwen3:0.6b", "gemma3:270m", "deepseek-v3.1:671b-cloud"],
        description="Fallback models to try if primary fails"
    )
    base_url: str = Field(default="http://127.0.0.1:11434", description="Ollama API URL")
    temperature: float = Field(default=0.1, description="Low temp for consistent reasoning")
    max_tokens: int = Field(default=2048, description="Max output tokens")
    timeout: int = Field(default=30, description="Request timeout in seconds")


class EDAConfig(BaseModel):
    """EDA probe thresholds and settings."""
    # Outlier detection
    zscore_threshold: float = Field(default=3.0, description="Z-score outlier threshold")
    iqr_multiplier: float = Field(default=1.5, description="IQR outlier multiplier")
    hampel_window: int = Field(default=5, description="Hampel filter window size")
    hampel_threshold: float = Field(default=3.0, description="Hampel MAD threshold")
    
    # Temporal analysis
    rolling_window: int = Field(default=24, description="Rolling window for temporal analysis")
    trend_min_periods: int = Field(default=10, description="Min periods for trend detection")
    autocorr_lags: int = Field(default=48, description="Lags for autocorrelation")
    
    # Correlation
    correlation_threshold: float = Field(default=0.5, description="Significant correlation threshold")
    lagged_correlation_max_lag: int = Field(default=12, description="Max lag for correlation")
    
    # Distribution
    skewness_threshold: float = Field(default=1.0, description="High skewness threshold")
    kurtosis_threshold: float = Field(default=3.0, description="Excess kurtosis threshold")


class MissingnessConfig(BaseModel):
    """Missingness handling configuration."""
    # Gap classification
    short_gap_threshold_seconds: int = Field(default=300, description="5 min = short gap")
    medium_gap_threshold_seconds: int = Field(default=3600, description="1 hour = medium gap")
    
    # Imputation settings
    interpolation_max_gap: int = Field(default=5, description="Max consecutive NaNs to interpolate")
    rolling_median_window: int = Field(default=12, description="Window for rolling median")
    
    # Missingness thresholds
    high_missing_threshold: float = Field(default=0.20, description="20% = high missingness")
    critical_missing_threshold: float = Field(default=0.50, description="50% = critical")
    
    # Pattern detection
    burst_detection_window: int = Field(default=10, description="Window for burst detection")
    burst_threshold: float = Field(default=0.5, description="50% missing in window = burst")


class RAGConfig(BaseModel):
    """RAG integration settings."""
    collection_name: str = Field(default="genorai_insights", description="ChromaDB collection")
    embedding_model: str = Field(default="all-MiniLM-L6-v2", description="Sentence transformer")
    chunk_size: int = Field(default=500, description="Text chunk size")
    top_k: int = Field(default=5, description="Top K retrieval results")


class Settings(BaseModel):
    """Main settings container."""
    # Paths
    project_root: Path = Field(default=Path("D:/GenoraiRAG"))
    data_dir: Path = Field(default=Path("D:/GenoraiRAG/data"))
    logs_dir: Path = Field(default=Path("D:/GenoraiRAG/logs"))
    cache_dir: Path = Field(default=Path("D:/GenoraiRAG/cache"))
    
    # Component configs
    llm: LLMConfig = Field(default_factory=LLMConfig)
    eda: EDAConfig = Field(default_factory=EDAConfig)
    missingness: MissingnessConfig = Field(default_factory=MissingnessConfig)
    rag: RAGConfig = Field(default_factory=RAGConfig)
    
    # Global settings
    debug: bool = Field(default=False, description="Enable debug mode")
    audit_enabled: bool = Field(default=True, description="Enable audit trail")
    
    def ensure_directories(self):
        """Create necessary directories if they don't exist."""
        for dir_path in [self.data_dir, self.logs_dir, self.cache_dir]:
            dir_path.mkdir(parents=True, exist_ok=True)


# Global settings instance
settings = Settings()
settings.ensure_directories()
