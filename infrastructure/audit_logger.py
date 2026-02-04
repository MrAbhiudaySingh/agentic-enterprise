"""
Audit Logger - Traceable decisions with citations and governance tracking.

Ensures all agent decisions are:
- Fully traceable to data sources
- Attributed to specific agents and versions
- Reviewable for compliance
- Timestamped and immutable
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Callable
from datetime import datetime
from enum import Enum
import json
import hashlib
import threading


class DecisionType(Enum):
    """Types of decisions agents can make."""
    RECOMMENDATION = "recommendation"
    APPROVAL = "approval"
    REJECTION = "rejection"
    ESCALATION = "escalation"
    ALLOCATION = "allocation"
    FORECAST = "forecast"
    STRATEGY = "strategy"


class ConfidenceLevel(Enum):
    """Confidence levels for agent outputs."""
    VERY_LOW = "very_low"    # < 50%
    LOW = "low"              # 50-65%
    MEDIUM = "medium"        # 65-80%
    HIGH = "high"            # 80-90%
    VERY_HIGH = "very_high"  # > 90%


@dataclass
class Citation:
    """Reference to a data source or document."""
    source_type: str  # "database", "document", "calculation", "assumption", "external"
    source_id: str
    description: str
    value: Any
    timestamp: datetime
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "source_type": self.source_type,
            "source_id": self.source_id,
            "description": self.description,
            "value": self.value,
            "timestamp": self.timestamp.isoformat()
        }


@dataclass
class DecisionRecord:
    """
    Complete record of an agent decision.
    Immutable after creation (except for outcome tracking).
    """
    id: str
    timestamp: datetime
    agent_name: str
    agent_version: str
    decision_type: DecisionType
    prompt_id: str  # Links to original CEO prompt
    
    # Decision content
    decision: str
    rationale: str
    confidence: ConfidenceLevel
    confidence_score: float  # 0-1
    
    # Traceability
    citations: List[Citation] = field(default_factory=list)
    data_sources: List[str] = field(default_factory=list)
    # Uncertainty documentation
    what_would_change_mind: str = ""  # What evidence would change this decision
    
    assumptions: List[str] = field(default_factory=list)
    key_uncertainties: List[str] = field(default_factory=list)
    
    # Governance
    required_approvals: List[str] = field(default_factory=list)
    obtained_approvals: List[str] = field(default_factory=list)
    escalated_to: Optional[str] = None
    
    # Outcome tracking (updated post-decision)
    outcome: Optional[str] = None
    outcome_timestamp: Optional[datetime] = None
    outcome_notes: Optional[str] = None
    
    # Audit metadata
    hash: str = ""  # Integrity verification
    
    def compute_hash(self) -> str:
        """Compute hash for integrity verification."""
        content = f"{self.id}:{self.timestamp.isoformat()}:{self.agent_name}:{self.decision}"
        return hashlib.sha256(content.encode()).hexdigest()[:16]
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "timestamp": self.timestamp.isoformat(),
            "agent_name": self.agent_name,
            "agent_version": self.agent_version,
            "decision_type": self.decision_type.value,
            "prompt_id": self.prompt_id,
            "decision": self.decision,
            "rationale": self.rationale,
            "confidence": self.confidence.value,
            "confidence_score": self.confidence_score,
            "citations": [c.to_dict() for c in self.citations],
            "data_sources": self.data_sources,
            "assumptions": self.assumptions,
            "what_would_change_mind": self.what_would_change_mind,
            "key_uncertainties": self.key_uncertainties,
            "required_approvals": self.required_approvals,
            "obtained_approvals": self.obtained_approvals,
            "escalated_to": self.escalated_to,
            "outcome": self.outcome,
            "outcome_timestamp": self.outcome_timestamp.isoformat() if self.outcome_timestamp else None,
            "outcome_notes": self.outcome_notes,
            "hash": self.hash
        }


class AuditLogger:
    """
    Central audit logging system for all agent decisions.
    
    Provides:
    - Immutable decision records
    - Full traceability to data sources
    - Confidence level tracking
    - Approval workflow tracking
    - Compliance reporting
    """
    
    def __init__(self):
        self._records: Dict[str, DecisionRecord] = {}
        self._prompt_index: Dict[str, List[str]] = {}  # prompt_id -> record_ids
        self._agent_index: Dict[str, List[str]] = {}   # agent_name -> record_ids
        self._callbacks: List[Callable[[DecisionRecord], None]] = []
        self._lock = threading.RLock()
        self._counter = 0
    
    def _generate_id(self) -> str:
        """Generate unique audit ID."""
        with self._lock:
            self._counter += 1
            return f"AUD-{datetime.now().strftime('%Y%m%d')}-{self._counter:06d}"
    
    def log_decision(
        self,
        agent_name: str,
        agent_version: str,
        decision_type: DecisionType,
        prompt_id: str,
        decision: str,
        rationale: str,
        confidence_score: float,
        citations: List[Citation],
        data_sources: List[str],
        assumptions: List[str],
        what_would_change_mind: str,
        key_uncertainties: List[str] = None,
        required_approvals: List[str] = None,
        escalated_to: Optional[str] = None
    ) -> DecisionRecord:
        """
        Log a new decision to the audit trail.
        
        Args:
            agent_name: Name of the agent making the decision
            agent_version: Version identifier for the agent
            decision_type: Type of decision
            prompt_id: Original prompt that triggered this
            decision: The actual decision text
            rationale: Explanation of reasoning
            confidence_score: 0-1 confidence level
            citations: List of data citations
            data_sources: List of data source identifiers
            assumptions: List of assumptions made
            what_would_change_mind: What would change this decision
            key_uncertainties: List of key uncertainties
            required_approvals: List of required approvers
            escalated_to: If escalated, to whom
            
        Returns:
            The created DecisionRecord
        """
        with self._lock:
            # Determine confidence level
            if confidence_score >= 0.9:
                confidence = ConfidenceLevel.VERY_HIGH
            elif confidence_score >= 0.8:
                confidence = ConfidenceLevel.HIGH
            elif confidence_score >= 0.65:
                confidence = ConfidenceLevel.MEDIUM
            elif confidence_score >= 0.5:
                confidence = ConfidenceLevel.LOW
            else:
                confidence = ConfidenceLevel.VERY_LOW
            
            record = DecisionRecord(
                id=self._generate_id(),
                timestamp=datetime.now(),
                agent_name=agent_name,
                agent_version=agent_version,
                decision_type=decision_type,
                prompt_id=prompt_id,
                decision=decision,
                rationale=rationale,
                confidence=confidence,
                confidence_score=confidence_score,
                citations=citations,
                data_sources=data_sources,
                assumptions=assumptions or [],
                what_would_change_mind=what_would_change_mind,
                key_uncertainties=key_uncertainties or [],
                required_approvals=required_approvals or [],
                escalated_to=escalated_to
            )
            
            # Compute and store hash
            record.hash = record.compute_hash()
            
            # Store record
            self._records[record.id] = record
            
            # Update indexes
            if prompt_id not in self._prompt_index:
                self._prompt_index[prompt_id] = []
            self._prompt_index[prompt_id].append(record.id)
            
            if agent_name not in self._agent_index:
                self._agent_index[agent_name] = []
            self._agent_index[agent_name].append(record.id)
            
            # Notify callbacks
            for callback in self._callbacks:
                try:
                    callback(record)
                except Exception:
                    pass
            
            return record
    
    def update_outcome(
        self,
        record_id: str,
        outcome: str,
        notes: Optional[str] = None
    ) -> bool:
        """
        Update the outcome of a decision.
        Only mutable field post-creation.
        """
        with self._lock:
            if record_id not in self._records:
                return False
            
            record = self._records[record_id]
            record.outcome = outcome
            record.outcome_timestamp = datetime.now()
            record.outcome_notes = notes
            return True
    
    def add_approval(self, record_id: str, approver: str) -> bool:
        """Record an approval for a decision."""
        with self._lock:
            if record_id not in self._records:
                return False
            
            record = self._records[record_id]
            if approver not in record.obtained_approvals:
                record.obtained_approvals.append(approver)
            return True
    
    def get_record(self, record_id: str) -> Optional[DecisionRecord]:
        """Get a specific decision record."""
        with self._lock:
            return self._records.get(record_id)
    
    def get_records_by_prompt(self, prompt_id: str) -> List[DecisionRecord]:
        """Get all decisions for a specific prompt."""
        with self._lock:
            record_ids = self._prompt_index.get(prompt_id, [])
            return [self._records[rid] for rid in record_ids if rid in self._records]
    
    def get_records_by_agent(self, agent_name: str) -> List[DecisionRecord]:
        """Get all decisions from a specific agent."""
        with self._lock:
            record_ids = self._agent_index.get(agent_name, [])
            return [self._records[rid] for rid in record_ids if rid in self._records]
    
    def get_pending_approvals(self) -> List[DecisionRecord]:
        """Get decisions awaiting approval."""
        with self._lock:
            pending = []
            for record in self._records.values():
                if record.required_approvals:
                    missing = set(record.required_approvals) - set(record.obtained_approvals)
                    if missing:
                        pending.append(record)
            return pending
    
    def get_escalated_decisions(self) -> List[DecisionRecord]:
        """Get decisions that were escalated."""
        with self._lock:
            return [r for r in self._records.values() if r.escalated_to]
    
    def verify_integrity(self, record_id: str) -> bool:
        """Verify the integrity of a record using its hash."""
        with self._lock:
            record = self._records.get(record_id)
            if not record:
                return False
            return record.hash == record.compute_hash()
    
    def generate_report(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        agent: Optional[str] = None
    ) -> Dict[str, Any]:
        """Generate an audit report."""
        with self._lock:
            records = list(self._records.values())
            
            if start_date:
                records = [r for r in records if r.timestamp >= start_date]
            if end_date:
                records = [r for r in records if r.timestamp <= end_date]
            if agent:
                records = [r for r in records if r.agent_name == agent]
            
            total = len(records)
            if total == 0:
                return {"total_decisions": 0}
            
            by_type = {}
            by_confidence = {}
            for r in records:
                dt = r.decision_type.value
                by_type[dt] = by_type.get(dt, 0) + 1
                
                cf = r.confidence.value
                by_confidence[cf] = by_confidence.get(cf, 0) + 1
            
            avg_confidence = sum(r.confidence_score for r in records) / total
            
            pending_approval = len([r for r in records if r.required_approvals and not r.obtained_approvals])
            escalated = len([r for r in records if r.escalated_to])
            
            return {
                "total_decisions": total,
                "date_range": {
                    "start": min(r.timestamp for r in records).isoformat(),
                    "end": max(r.timestamp for r in records).isoformat()
                },
                "by_type": by_type,
                "by_confidence": by_confidence,
                "average_confidence": round(avg_confidence, 3),
                "pending_approvals": pending_approval,
                "escalated": escalated,
                "agents": list(set(r.agent_name for r in records))
            }
    
    def export_json(self, filepath: str) -> None:
        """Export all records to JSON file."""
        with self._lock:
            data = {
                "exported_at": datetime.now().isoformat(),
                "record_count": len(self._records),
                "records": [r.to_dict() for r in self._records.values()]
            }
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2)
    
    def register_callback(self, callback: Callable[[DecisionRecord], None]) -> None:
        """Register callback for new decisions."""
        with self._lock:
            self._callbacks.append(callback)


# Singleton instance
_audit_logger = None

def get_audit_logger() -> AuditLogger:
    """Get the singleton audit logger instance."""
    global _audit_logger
    if _audit_logger is None:
        _audit_logger = AuditLogger()
    return _audit_logger


if __name__ == "__main__":
    # Test the audit logger
    logger = get_audit_logger()
    
    # Log a test decision
    record = logger.log_decision(
        agent_name="finance_agent",
        agent_version="1.0.0",
        decision_type=DecisionType.RECOMMENDATION,
        prompt_id="PROMPT-001",
        decision="Approve $150K marketing budget increase",
        rationale="ROI analysis shows 3.2x return based on historical campaign data",
        confidence_score=0.85,
        citations=[
            Citation(
                source_type="database",
                source_id="campaign_roi_q3",
                description="Q3 campaign performance metrics",
                value={"avg_roi": 3.2, "sample_size": 12},
                timestamp=datetime.now()
            )
        ],
        data_sources=["marketing_db", "finance_erp"],
        assumptions=["Historical performance is predictive of future results"],
        what_would_change_mind="Evidence that CAC has increased by >20% in last 30 days",
        key_uncertainties=["Competitive pricing pressure", "Economic conditions"],
        required_approvals=["CFO", "CMO"]
    )
    
    print("=== Audit Logger Test ===\n")
    print(f"Record ID: {record.id}")
    print(f"Hash: {record.hash}")
    print(f"Confidence: {record.confidence.value} ({record.confidence_score:.0%})")
    print(f"Citations: {len(record.citations)}")
    print(f"Required approvals: {record.required_approvals}")
    
    # Add approval
    logger.add_approval(record.id, "CFO")
    print(f"\nAfter CFO approval:")
    print(f"Obtained: {logger.get_record(record.id).obtained_approvals}")
    
    # Generate report
    report = logger.generate_report()
    print(f"\nAudit Report:")
    print(f"  Total decisions: {report['total_decisions']}")
    print(f"  Avg confidence: {report['average_confidence']:.1%}")
