"""
Base Agent Class

Abstract base class that all functional agents inherit from.
Provides common functionality for task processing, logging, and uncertainty quantification.
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import uuid


@dataclass
class AgentOutput:
    """Standardized output format for all agents."""
    agent_name: str
    task_id: str
    recommendations: List[Dict[str, Any]]
    confidence: float  # 0-1
    citations: List[str]  # Data sources cited
    what_would_change_mind: List[str] = None  # Conditions that would change recommendation
    budget_impact: Optional[float] = None
    headcount_impact: Optional[int] = None
    timeline_days: Optional[int] = None
    risks: List[str] = None
    dependencies: List[str] = None
    
    def __post_init__(self):
        if self.risks is None:
            self.risks = []
        if self.dependencies is None:
            self.dependencies = []
        if self.what_would_change_mind is None:
            self.what_would_change_mind = []


class BaseAgent(ABC):
    """
    Abstract base class for all enterprise functional agents.
    
    All agents must implement:
    - process_task(): Main entry point for task execution
    
    Common functionality provided:
    - Shared memory access
    - Audit logging
    - Data citations
    - Confidence scoring
    """
    
    def __init__(self, agent_name: str):
        self.agent_name = agent_name
        self._task_count = 0
    
    @abstractmethod
    def process_task(self, task: Dict[str, Any], 
                     shared_memory: Any,
                     enterprise_data: Any,
                     audit_logger: Any) -> AgentOutput:
        """
        Process a task assigned by the CEO orchestrator.
        
        Args:
            task: Task specification from orchestrator
            shared_memory: Shared memory instance
            enterprise_data: Enterprise data access
            audit_logger: Audit logger instance
            
        Returns:
            AgentOutput with recommendations and metadata
        """
        pass
    
    def _generate_task_id(self) -> str:
        """Generate a unique task ID."""
        self._task_count += 1
        return f"{self.agent_name.upper()}-{self._task_count:04d}-{uuid.uuid4().hex[:6]}"
    
    def _cite_data_source(self, source: str, query: str, 
                          records: int) -> str:
        """Generate a citation for data access."""
        return f"{source}:{query}:{records}_records"
    
    def _format_recommendation(self, title: str, description: str,
                               expected_impact: str, action_items: List[str]) -> Dict[str, Any]:
        """Format a recommendation consistently."""
        return {
            "title": title,
            "description": description,
            "expected_impact": expected_impact,
            "action_items": action_items
        }
    
    def _assess_confidence(self, data_quality: float, 
                          assumptions_made: int,
                          historical_precedent: bool) -> float:
        """
        Calculate confidence score based on data quality and assumptions.
        
        Args:
            data_quality: 0-1 score of data completeness/accuracy
            assumptions_made: Number of assumptions required
            historical_precedent: Whether similar actions succeeded before
            
        Returns:
            Confidence score 0-1
        """
        base_confidence = data_quality
        
        # Reduce confidence for each assumption
        assumption_penalty = min(0.3, assumptions_made * 0.05)
        base_confidence -= assumption_penalty
        
        # Boost if historical precedent exists
        if historical_precedent:
            base_confidence = min(1.0, base_confidence + 0.1)
        
        return max(0.0, min(1.0, base_confidence))
    
    def _identify_change_conditions(self, output: AgentOutput) -> List[str]:
        """
        Identify what conditions would change the recommendation.
        Default implementation - override for domain-specific logic.
        """
        return [
            "Significant change in market conditions",
            "New competitive intelligence",
            "Regulatory changes affecting the approach",
            "Budget constraints tighter than anticipated"
        ]
    
    def _log_decision(self, audit_logger: Any, decision: str, 
                     reasoning: str, citations: List[str],
                     confidence: float) -> str:
        """Log a decision to the audit trail."""
        return audit_logger.log_decision(
            agent=self.agent_name,
            decision=decision,
            reasoning=reasoning,
            citations=citations,
            confidence=confidence
        )
    
    def _access_data(self, audit_logger: Any, data_source: str,
                    query: str, records: int, purpose: str) -> str:
        """Log data access and return citation."""
        audit_logger.log_data_access(
            agent=self.agent_name,
            data_source=data_source,
            query=query,
            records_accessed=records,
            purpose=purpose
        )
        return self._cite_data_source(data_source, query, records)
