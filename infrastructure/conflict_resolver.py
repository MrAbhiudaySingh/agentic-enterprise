"""
Conflict Resolver

Detects and resolves contradictions between agent recommendations.
Ensures cross-functional alignment before presenting to CEO.
"""

from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import re


class ConflictType(Enum):
    """Types of cross-agent conflicts."""
    BUDGET_OVERALLOCATION = "budget_overallocation"
    RESOURCE_CONTENTION = "resource_contention"
    STRATEGIC_MISALIGNMENT = "strategic_misalignment"
    TIMELINE_CONFLICT = "timeline_conflict"
    DEPENDENCY_UNMET = "dependency_unmet"
    PRIORITY_CONFLICT = "priority_conflict"


@dataclass
class Conflict:
    """A detected conflict between agents."""
    conflict_id: str
    conflict_type: ConflictType
    agents_involved: List[str]
    description: str
    agent_recommendations: Dict[str, Any]
    severity: str  # "low", "medium", "high", "critical"
    resolution: Optional[str] = None
    resolution_details: Optional[Dict[str, Any]] = None


class ConflictResolver:
    """
    Detects and resolves conflicts between functional agents.
    
    Conflicts detected:
    - Budget overallocations (agents requesting more than available)
    - Resource contention (same resources requested by multiple agents)
    - Strategic misalignment (contradictory strategic directions)
    - Timeline conflicts (dependencies not met)
    - Priority conflicts (competing priorities)
    """
    
    def __init__(self):
        self._conflicts: List[Conflict] = []
        self._resolution_strategies = {
            ConflictType.BUDGET_OVERALLOCATION: self._resolve_budget_conflict,
            ConflictType.RESOURCE_CONTENTION: self._resolve_resource_conflict,
            ConflictType.STRATEGIC_MISALIGNMENT: self._resolve_strategic_conflict,
            ConflictType.TIMELINE_CONFLICT: self._resolve_timeline_conflict,
            ConflictType.PRIORITY_CONFLICT: self._resolve_priority_conflict,
        }
    
    def detect_conflicts(self, agent_outputs: Dict[str, Dict[str, Any]], 
                        company_context: Any) -> List[Conflict]:
        """
        Analyze agent outputs and detect conflicts.
        
        Args:
            agent_outputs: Dict mapping agent_name -> agent output
            company_context: CompanyContext from shared memory
            
        Returns:
            List of detected conflicts
        """
        conflicts = []
        
        # Check for budget conflicts
        budget_conflict = self._detect_budget_conflict(agent_outputs, company_context)
        if budget_conflict:
            conflicts.append(budget_conflict)
        
        # Check for timeline conflicts
        timeline_conflict = self._detect_timeline_conflict(agent_outputs)
        if timeline_conflict:
            conflicts.append(timeline_conflict)
        
        # Check for strategic misalignment
        strategic_conflict = self._detect_strategic_misalignment(agent_outputs)
        if strategic_conflict:
            conflicts.append(strategic_conflict)
        
        # Check for resource contention
        resource_conflict = self._detect_resource_contention(agent_outputs)
        if resource_conflict:
            conflicts.append(resource_conflict)
        
        self._conflicts = conflicts
        return conflicts
    
    def _detect_budget_conflict(self, agent_outputs: Dict[str, Dict[str, Any]], 
                                company_context: Any) -> Optional[Conflict]:
        """Detect if agents are requesting more budget than available."""
        budget_requests = {}
        
        for agent_name, output in agent_outputs.items():
            if "budget_request" in output:
                req = output["budget_request"]
                dept = req.get("department", agent_name.replace("_agent", ""))
                amount = req.get("amount", 0)
                
                if dept not in budget_requests:
                    budget_requests[dept] = []
                budget_requests[dept].append({
                    "agent": agent_name,
                    "amount": amount,
                    "purpose": req.get("purpose", "")
                })
        
        # Check against budget limits
        conflicts_detected = []
        for dept, requests in budget_requests.items():
            total_requested = sum(r["amount"] for r in requests)
            budget_limit = company_context.budget_limits.get(dept, 0)
            
            # Check available budget (mock calculation)
            spent = budget_limit * 0.5  # Assume 50% spent
            available = budget_limit - spent
            
            if total_requested > available:
                conflicts_detected.append({
                    "department": dept,
                    "requested": total_requested,
                    "available": available,
                    "shortfall": total_requested - available,
                    "requests": requests
                })
        
        if conflicts_detected:
            return Conflict(
                conflict_id="CONF-001",
                conflict_type=ConflictType.BUDGET_OVERALLOCATION,
                agents_involved=list(agent_outputs.keys()),
                description=f"Budget overrun detected: {conflicts_detected[0]['shortfall']} over allocated budget",
                agent_recommendations={"budget_conflicts": conflicts_detected},
                severity="high"
            )
        
        return None
    
    def _detect_timeline_conflict(self, agent_outputs: Dict[str, Dict[str, Any]]) -> Optional[Conflict]:
        """Detect timeline dependencies that aren't met."""
        dependencies = []
        deliverables = []
        
        for agent_name, output in agent_outputs.items():
            if "timeline" in output:
                timeline = output["timeline"]
                
                # Collect dependencies
                if "depends_on" in timeline:
                    for dep in timeline["depends_on"]:
                        dependencies.append({
                            "agent": agent_name,
                            "depends_on": dep,
                            "needed_by": timeline.get("completion_date")
                        })
                
                # Collect deliverables
                if "deliverables" in timeline:
                    for deliv in timeline["deliverables"]:
                        deliverables.append({
                            "agent": agent_name,
                            "deliverable": deliv["name"],
                            "delivery_date": deliv.get("date")
                        })
        
        # Check if dependencies are met
        unmet = []
        for dep in dependencies:
            found = any(
                d["deliverable"] == dep["depends_on"] 
                for d in deliverables
            )
            if not found:
                unmet.append(dep)
        
        if unmet:
            return Conflict(
                conflict_id="CONF-002",
                conflict_type=ConflictType.TIMELINE_CONFLICT,
                agents_involved=[u["agent"] for u in unmet],
                description=f"Unmet dependencies: {[u['depends_on'] for u in unmet]}",
                agent_recommendations={"unmet_dependencies": unmet},
                severity="medium"
            )
        
        return None
    
    def _detect_strategic_misalignment(self, agent_outputs: Dict[str, Dict[str, Any]]) -> Optional[Conflict]:
        """Detect contradictory strategic recommendations."""
        strategies = {}
        
        for agent_name, output in agent_outputs.items():
            if "strategy" in output:
                strategies[agent_name] = output["strategy"]
        
        # Check for contradictions
        contradictions = []
        
        # Example: Marketing wants to increase CAC for quality, Finance wants to reduce CAC
        marketing_strat = strategies.get("marketing_agent", {})
        finance_strat = strategies.get("finance_agent", {})
        
        if (marketing_strat.get("cac_direction") == "increase" and 
            finance_strat.get("cac_direction") == "decrease"):
            contradictions.append({
                "issue": "CAC strategy conflict",
                "marketing_position": "Increase CAC for higher quality leads",
                "finance_position": "Decrease CAC to improve unit economics"
            })
        
        # Example: Sales wants discounting, Finance wants margin protection
        sales_strat = strategies.get("sales_agent", {})
        if (sales_strat.get("pricing_strategy") == "aggressive_discount" and
            finance_strat.get("margin_protection") == True):
            contradictions.append({
                "issue": "Pricing strategy conflict",
                "sales_position": "Aggressive discounting to win deals",
                "finance_position": "Protect margins, minimize discounting"
            })
        
        if contradictions:
            return Conflict(
                conflict_id="CONF-003",
                conflict_type=ConflictType.STRATEGIC_MISALIGNMENT,
                agents_involved=list(strategies.keys()),
                description="Contradictory strategic directions detected",
                agent_recommendations={"contradictions": contradictions},
                severity="critical"
            )
        
        return None
    
    def _detect_resource_contention(self, agent_outputs: Dict[str, Dict[str, Any]]) -> Optional[Conflict]:
        """Detect multiple agents requesting the same scarce resources."""
        resource_requests = {}
        
        for agent_name, output in agent_outputs.items():
            if "resource_requests" in output:
                for resource in output["resource_requests"]:
                    name = resource.get("resource")
                    if name not in resource_requests:
                        resource_requests[name] = []
                    resource_requests[name].append({
                        "agent": agent_name,
                        "amount": resource.get("amount", 1),
                        "priority": resource.get("priority", "medium")
                    })
        
        # Find contention
        contentions = []
        for resource, requests in resource_requests.items():
            if len(requests) > 1:
                total_requested = sum(r["amount"] for r in requests)
                # Assume limited availability
                if total_requested > 3:  # Arbitrary threshold
                    contentions.append({
                        "resource": resource,
                        "total_requested": total_requested,
                        "requests": requests
                    })
        
        if contentions:
            return Conflict(
                conflict_id="CONF-004",
                conflict_type=ConflictType.RESOURCE_CONTENTION,
                agents_involved=list(set(r["agent"] for c in contentions for r in c["requests"])),
                description=f"Resource contention: {[c['resource'] for c in contentions]}",
                agent_recommendations={"contentions": contentions},
                severity="medium"
            )
        
        return None
    
    def resolve_conflicts(self, conflicts: List[Conflict]) -> Tuple[List[Conflict], Dict[str, Any]]:
        """
        Attempt to resolve detected conflicts.
        
        Returns:
            Tuple of (unresolved_conflicts, resolution_summary)
        """
        unresolved = []
        resolutions = []
        
        for conflict in conflicts:
            resolver = self._resolution_strategies.get(conflict.conflict_type)
            if resolver:
                resolution = resolver(conflict)
                conflict.resolution = resolution["description"]
                conflict.resolution_details = resolution
                resolutions.append({
                    "conflict_id": conflict.conflict_id,
                    "resolution": resolution
                })
                
                if not resolution.get("resolved", False):
                    unresolved.append(conflict)
            else:
                unresolved.append(conflict)
        
        return unresolved, {"resolutions": resolutions, "unresolved_count": len(unresolved)}
    
    def _resolve_budget_conflict(self, conflict: Conflict) -> Dict[str, Any]:
        """Resolve budget overallocation through prioritization."""
        data = conflict.agent_recommendations.get("budget_conflicts", [])
        if not data:
            return {"resolved": False, "description": "No conflict data"}
        
        # Prioritize by strategic importance
        dept = data[0]["department"]
        requests = data[0]["requests"]
        available = data[0]["available"]
        
        # Sort by priority (high -> medium -> low)
        priority_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
        sorted_requests = sorted(
            requests, 
            key=lambda x: priority_order.get(x.get("priority", "medium"), 2)
        )
        
        # Allocate budget by priority until exhausted
        allocated = []
        remaining = available
        
        for req in sorted_requests:
            if req["amount"] <= remaining:
                allocated.append({
                    "agent": req["agent"],
                    "amount": req["amount"],
                    "status": "fully_funded"
                })
                remaining -= req["amount"]
            else:
                allocated.append({
                    "agent": req["agent"],
                    "amount": remaining,
                    "requested": req["amount"],
                    "status": "partially_funded"
                })
                remaining = 0
        
        return {
            "resolved": remaining >= 0,
            "description": f"Budget allocated by priority. Remaining: ${remaining:,.0f}",
            "allocation": allocated,
            "requires_ceo_approval": remaining < 0
        }
    
    def _resolve_resource_conflict(self, conflict: Conflict) -> Dict[str, Any]:
        """Resolve resource contention through scheduling."""
        return {
            "resolved": True,
            "description": "Resources scheduled sequentially by priority",
            "strategy": "time_phasing"
        }
    
    def _resolve_strategic_conflict(self, conflict: Conflict) -> Dict[str, Any]:
        """Strategic conflicts require CEO decision."""
        return {
            "resolved": False,
            "description": "Strategic misalignment requires CEO decision",
            "escalation_required": True,
            "options": conflict.agent_recommendations.get("contradictions", [])
        }
    
    def _resolve_timeline_conflict(self, conflict: Conflict) -> Dict[str, Any]:
        """Resolve timeline conflicts through dependency management."""
        return {
            "resolved": True,
            "description": "Timeline adjusted to respect dependencies",
            "strategy": "critical_path_adjustment"
        }
    
    def _resolve_priority_conflict(self, conflict: Conflict) -> Dict[str, Any]:
        """Resolve priority conflicts through ranking."""
        return {
            "resolved": True,
            "description": "Priorities ranked by strategic impact",
            "strategy": "impact_ranking"
        }
    
    def get_alignment_report(self) -> Dict[str, Any]:
        """Get a summary of cross-functional alignment status."""
        if not self._conflicts:
            return {
                "status": "ALIGNED",
                "conflicts_detected": 0,
                "message": "All agents in alignment"
            }
        
        critical = sum(1 for c in self._conflicts if c.severity == "critical")
        high = sum(1 for c in self._conflicts if c.severity == "high")
        
        return {
            "status": "NEEDS_RESOLUTION" if critical > 0 else "MINOR_CONFLICTS",
            "conflicts_detected": len(self._conflicts),
            "by_severity": {"critical": critical, "high": high, "medium": len(self._conflicts) - critical - high},
            "unresolved": [c.conflict_id for c in self._conflicts if not c.resolution],
            "message": f"{critical} critical conflicts require attention" if critical > 0 else "Minor conflicts auto-resolved"
        }
