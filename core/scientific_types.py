"""
Core scientific types for GenoraiRAG.
Defines the fundamental structures for Hypothesis, Evidence, and Confidence.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Dict, Any, Optional
from datetime import datetime
import hashlib
import json

class EvidenceType(str, Enum):
    STATISTICAL = "statistical"
    CAUSAL = "causal"
    CORRELATIONAL = "correlational"
    OBSERVATIONAL = "observational"
    LITERATURE = "literature"

class HypothesisStatus(str, Enum):
    PROPOSED = "proposed"
    TESTING = "testing"
    VERIFIED = "verified"
    FALSIFIED = "falsified"
    INCONCLUSIVE = "inconclusive"

@dataclass
class Confidence:
    """
    Represents the statistical confidence of a finding.
    """
    score: float  # 0.0 to 1.0
    statistical_power: Optional[float] = None
    sample_size: Optional[int] = None
    p_value: Optional[float] = None
    margin_of_error: Optional[float] = None
    
    def __str__(self) -> str:
        base = f"{self.score:.1%}"
        if self.sample_size:
            base += f" (N={self.sample_size})"
        if self.p_value is not None:
            base += f" [p={self.p_value:.4f}]"
        return base

@dataclass
class Evidence:
    """
    A unit of scientific evidence produced by a probe or experiment.
    """
    type: EvidenceType
    content: str
    data: Dict[str, Any]
    confidence: Confidence
    source_probe: str
    timestamp: datetime = field(default_factory=datetime.now)
    dependencies: List[str] = field(default_factory=list)  # IDs of other evidence/data
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    @property
    def id(self) -> str:
        """Deterministic hash of the evidence content and data."""
        payload = f"{self.type}:{self.content}:{json.dumps(self.data, sort_keys=True)}"
        return hashlib.sha256(payload.encode()).hexdigest()[:16]

@dataclass
class Experiment:
    """
    A planned procedure to test a hypothesis.
    """
    name: str
    probes: List[str]
    parameters: Dict[str, Any]
    expected_outcome: Optional[str] = None
    
@dataclass
class Hypothesis:
    """
    A proposed explanation to be tested.
    """
    statement: str
    null_hypothesis: str
    id: str = field(default_factory=lambda: hashlib.sha256(str(datetime.now().isoformat()).encode()).hexdigest()[:8])
    status: HypothesisStatus = HypothesisStatus.PROPOSED
    experiments: List[Experiment] = field(default_factory=list)
    supporting_evidence: List[Evidence] = field(default_factory=list)
    contradicting_evidence: List[Evidence] = field(default_factory=list)
    confidence: float = 0.0
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    
    def add_evidence(self, evidence: Evidence, supports: bool):
        if supports:
            self.supporting_evidence.append(evidence)
        else:
            self.contradicting_evidence.append(evidence)
        self.updated_at = datetime.now()
        self._recalculate_confidence()
        
    def _recalculate_confidence(self):
        # Rough heuristic: confidence increases with supporting evidence, decreases with contradictions
        # This will be replaced by a more sophisticated Bayesian update in the future
        support_score = sum(e.confidence.score for e in self.supporting_evidence)
        contradict_score = sum(e.confidence.score for e in self.contradicting_evidence)
        
        total = support_score + contradict_score
        if total == 0:
            self.confidence = 0.0
            return

        balance = (support_score - contradict_score) / total
        # Normalize to 0-1 range roughly
        self.confidence = max(0.0, min(1.0, 0.5 + (balance * 0.5)))
