"""
Shared Memory - Central state management for company goals, policies, constraints, and agent outputs.

This module provides a thread-safe shared memory system for inter-agent communication
and persistent state across the enterprise operating model.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Callable
from datetime import datetime
from enum import Enum
import threading
import json


class MemoryType(Enum):
    """Types of memory entries."""
    GOAL = "goal"
    POLICY = "policy"
    CONSTRAINT = "constraint"
    AGENT_OUTPUT = "agent_output"
    DECISION = "decision"
    ALERT = "alert"
    CONTEXT = "context"


class Priority(Enum):
    """Priority levels for memory entries."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class MemoryEntry:
    """A single entry in shared memory."""
    id: str
    type: MemoryType
    source: str  # Agent or system that created this
    content: Dict[str, Any]
    timestamp: datetime
    priority: Priority
    tags: List[str] = field(default_factory=list)
    references: List[str] = field(default_factory=list)  # IDs of related entries
    expires_at: Optional[datetime] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "id": self.id,
            "type": self.type.value,
            "source": self.source,
            "content": self.content,
            "timestamp": self.timestamp.isoformat(),
            "priority": self.priority.value,
            "tags": self.tags,
            "references": self.references,
            "expires_at": self.expires_at.isoformat() if self.expires_at else None
        }


@dataclass
class CompanyGoal:
    """Structured company goal."""
    id: str
    description: str
    target_value: float
    current_value: float
    unit: str
    deadline: datetime
    owner: str
    status: str  # "active", "at_risk", "achieved", "missed"
    associated_agents: List[str] = field(default_factory=list)
    key_results: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class Constraint:
    """Business constraint (budget, headcount, regulatory, etc.)."""
    id: str
    category: str  # "budget", "headcount", "regulatory", "technical", "time"
    description: str
    limit_value: float
    current_usage: float
    unit: str
    hard_limit: bool  # True = cannot be exceeded, False = soft limit with approval
    owner: str


class SharedMemory:
    """
    Central shared memory for the agentic enterprise.
    
    Thread-safe storage for:
    - Company goals and OKRs
    - Business policies and rules
    - Constraints (budget, headcount, etc.)
    - Agent outputs and recommendations
    - Cross-agent context
    """
    
    def __init__(self):
        self._entries: Dict[str, MemoryEntry] = {}
        self._goals: Dict[str, CompanyGoal] = {}
        self._constraints: Dict[str, Constraint] = {}
        self._callbacks: List[Callable[[MemoryEntry], None]] = []
        self._lock = threading.RLock()
        self._counter = 0
    
    def _generate_id(self) -> str:
        """Generate a unique ID."""
        with self._lock:
            self._counter += 1
            return f"MEM-{datetime.now().strftime('%Y%m%d')}-{self._counter:06d}"
    
    def store(
        self,
        type: MemoryType,
        source: str,
        content: Dict[str, Any],
        priority: Priority = Priority.MEDIUM,
        tags: List[str] = None,
        references: List[str] = None,
        expires_in_hours: Optional[int] = None
    ) -> str:
        """
        Store a new entry in shared memory.
        
        Args:
            type: Type of memory entry
            source: Source agent or system
            content: Content dictionary
            priority: Priority level
            tags: Optional tags for categorization
            references: IDs of related entries
            expires_in_hours: Optional expiration time
            
        Returns:
            ID of the created entry
        """
        with self._lock:
            entry_id = self._generate_id()
            expires = None
            if expires_in_hours:
                expires = datetime.now() + timedelta(hours=expires_in_hours)
            
            entry = MemoryEntry(
                id=entry_id,
                type=type,
                source=source,
                content=content,
                timestamp=datetime.now(),
                priority=priority,
                tags=tags or [],
                references=references or [],
                expires_at=expires
            )
            
            self._entries[entry_id] = entry
            
            # Notify callbacks
            for callback in self._callbacks:
                try:
                    callback(entry)
                except Exception:
                    pass
            
            return entry_id
    
    def get(self, entry_id: str) -> Optional[MemoryEntry]:
        """Get a specific entry by ID."""
        with self._lock:
            return self._entries.get(entry_id)
    
    def query(
        self,
        type: Optional[MemoryType] = None,
        source: Optional[str] = None,
        tags: Optional[List[str]] = None,
        min_priority: Optional[Priority] = None,
        since: Optional[datetime] = None
    ) -> List[MemoryEntry]:
        """
        Query entries with filters.
        
        Args:
            type: Filter by entry type
            source: Filter by source
            tags: Filter by tags (all must match)
            min_priority: Minimum priority level
            since: Only entries after this timestamp
            
        Returns:
            List of matching entries, sorted by timestamp desc
        """
        with self._lock:
            results = []
            for entry in self._entries.values():
                # Check expiration
                if entry.expires_at and entry.expires_at < datetime.now():
                    continue
                
                # Apply filters
                if type and entry.type != type:
                    continue
                if source and entry.source != source:
                    continue
                if tags and not all(tag in entry.tags for tag in tags):
                    continue
                if min_priority and entry.priority.value < min_priority.value:
                    continue
                if since and entry.timestamp < since:
                    continue
                
                results.append(entry)
            
            return sorted(results, key=lambda e: e.timestamp, reverse=True)
    
    def add_goal(self, goal: CompanyGoal) -> None:
        """Add or update a company goal."""
        with self._lock:
            self._goals[goal.id] = goal
            self.store(
                type=MemoryType.GOAL,
                source="system",
                content={
                    "goal_id": goal.id,
                    "description": goal.description,
                    "target": goal.target_value,
                    "current": goal.current_value,
                    "unit": goal.unit,
                    "status": goal.status,
                    "deadline": goal.deadline.isoformat()
                },
                priority=Priority.HIGH,
                tags=["goal", goal.status]
            )
    
    def get_goal(self, goal_id: str) -> Optional[CompanyGoal]:
        """Get a specific goal."""
        with self._lock:
            return self._goals.get(goal_id)
    
    def get_active_goals(self) -> List[CompanyGoal]:
        """Get all active goals."""
        with self._lock:
            return [g for g in self._goals.values() if g.status == "active"]
    
    def update_goal_progress(self, goal_id: str, new_value: float) -> None:
        """Update progress on a goal."""
        with self._lock:
            if goal_id in self._goals:
                self._goals[goal_id].current_value = new_value
    
    def add_constraint(self, constraint: Constraint) -> None:
        """Add a business constraint."""
        with self._lock:
            self._constraints[constraint.id] = constraint
            self.store(
                type=MemoryType.CONSTRAINT,
                source="system",
                content={
                    "constraint_id": constraint.id,
                    "category": constraint.category,
                    "description": constraint.description,
                    "limit": constraint.limit_value,
                    "current": constraint.current_usage,
                    "unit": constraint.unit,
                    "hard_limit": constraint.hard_limit
                },
                priority=Priority.HIGH if constraint.hard_limit else Priority.MEDIUM,
                tags=["constraint", constraint.category]
            )
    
    def get_constraint(self, constraint_id: str) -> Optional[Constraint]:
        """Get a specific constraint."""
        with self._lock:
            return self._constraints.get(constraint_id)
    
    def get_constraints_by_category(self, category: str) -> List[Constraint]:
        """Get constraints by category."""
        with self._lock:
            return [c for c in self._constraints.values() if c.category == category]
    
    def update_constraint_usage(self, constraint_id: str, new_usage: float) -> bool:
        """
        Update constraint usage. Returns False if hard limit exceeded.
        """
        with self._lock:
            if constraint_id not in self._constraints:
                return True
            
            constraint = self._constraints[constraint_id]
            constraint.current_usage = new_usage
            
            if constraint.hard_limit and new_usage > constraint.limit_value:
                self.store(
                    type=MemoryType.ALERT,
                    source="system",
                    content={
                        "alert_type": "constraint_violation",
                        "constraint_id": constraint_id,
                        "limit": constraint.limit_value,
                        "attempted": new_usage
                    },
                    priority=Priority.CRITICAL,
                    tags=["alert", "constraint_violation"]
                )
                return False
            
            return True
    
    def register_callback(self, callback: Callable[[MemoryEntry], None]) -> None:
        """Register a callback for new memory entries."""
        with self._lock:
            self._callbacks.append(callback)
    
    def get_agent_outputs(self, agent_name: Optional[str] = None) -> List[MemoryEntry]:
        """Get outputs from agents."""
        return self.query(
            type=MemoryType.AGENT_OUTPUT,
            source=agent_name
        )
    
    def get_recent_context(self, hours: int = 24) -> List[MemoryEntry]:
        """Get recent context entries."""
        since = datetime.now() - timedelta(hours=hours)
        return self.query(since=since)
    
    def export_snapshot(self) -> Dict[str, Any]:
        """Export current memory state as dictionary."""
        with self._lock:
            return {
                "timestamp": datetime.now().isoformat(),
                "entries_count": len(self._entries),
                "goals": {k: {
                    "id": g.id,
                    "description": g.description,
                    "target": g.target_value,
                    "current": g.current_value,
                    "unit": g.unit,
                    "status": g.status
                } for k, g in self._goals.items()},
                "constraints": {k: {
                    "id": c.id,
                    "category": c.category,
                    "limit": c.limit_value,
                    "current": c.current_usage,
                    "hard_limit": c.hard_limit
                } for k, c in self._constraints.items()},
                "recent_entries": [
                    e.to_dict() for e in self.query()[:20]
                ]
            }
    
    def clear_expired(self) -> int:
        """Clear expired entries. Returns count removed."""
        with self._lock:
            expired = [
                eid for eid, e in self._entries.items()
                if e.expires_at and e.expires_at < datetime.now()
            ]
            for eid in expired:
                del self._entries[eid]
            return len(expired)


# Import timedelta at the end to avoid circular issues
from datetime import timedelta

# Singleton instance
_shared_memory = None

def get_shared_memory() -> SharedMemory:
    """Get the singleton shared memory instance."""
    global _shared_memory
    if _shared_memory is None:
        _shared_memory = SharedMemory()
    return _shared_memory


if __name__ == "__main__":
    # Test the shared memory system
    memory = get_shared_memory()
    
    # Add some test data
    memory.store(
        type=MemoryType.CONTEXT,
        source="test",
        content={"message": "Hello, enterprise!"},
        tags=["test", "greeting"]
    )
    
    # Add a goal
    from datetime import datetime, timedelta
    goal = CompanyGoal(
        id="GOAL-001",
        description="Improve quarterly retention by 8%",
        target_value=0.92,
        current_value=0.84,
        unit="percentage",
        deadline=datetime.now() + timedelta(days=90),
        owner="CEO",
        status="active"
    )
    memory.add_goal(goal)
    
    # Add a constraint
    constraint = Constraint(
        id="CONST-001",
        category="budget",
        description="Q3 Marketing Budget",
        limit_value=500000,
        current_usage=320000,
        unit="USD",
        hard_limit=False,
        owner="CFO"
    )
    memory.add_constraint(constraint)
    
    # Query and display
    print("=== Shared Memory Test ===\n")
    print(f"Total entries: {len(memory._entries)}")
    print(f"Active goals: {len(memory.get_active_goals())}")
    print(f"Constraints: {len(memory._constraints)}")
    
    print("\nRecent entries:")
    for entry in memory.query()[:5]:
        print(f"  - {entry.type.value}: {entry.source} ({entry.priority.value})")
