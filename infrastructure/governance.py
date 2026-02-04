"""
Governance System

Manages permissions, approvals, and escalation rules for the Agentic Enterprise.
Ensures agents operate within authority boundaries.
"""

from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum


class PermissionLevel(Enum):
    """Authority levels for agents."""
    READ = "read"  # Can access data
    RECOMMEND = "recommend"  # Can make recommendations
    ACT = "act"  # Can take actions within limits
    APPROVE = "approve"  # Can approve requests


class ApprovalStatus(Enum):
    """Status of approval requests."""
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    ESCALATED = "escalated"
    AUTO_APPROVED = "auto_approved"


@dataclass
class ApprovalRequest:
    """A request for approval."""
    request_id: str
    requester: str  # Agent that made the request
    approver: str  # Who needs to approve
    request_type: str  # "budget", "hiring", "policy_change", etc.
    description: str
    amount: Optional[float] = None
    details: Dict[str, Any] = None
    status: ApprovalStatus = ApprovalStatus.PENDING
    conditions: List[str] = None
    
    def __post_init__(self):
        if self.conditions is None:
            self.conditions = []
        if self.details is None:
            self.details = {}


class Governance:
    """
    Governance system for the Agentic Enterprise.
    
    Manages:
    - Agent permission levels
    - Approval workflows
    - Auto-approval thresholds
    - Escalation rules
    """
    
    def __init__(self):
        self._agent_permissions: Dict[str, Dict[str, Any]] = {}
        self._approval_requests: List[ApprovalRequest] = []
        self._auto_approval_limits = {
            "budget": 50000,  # Auto-approve under $50K
            "hiring": 3,      # Auto-approve under 3 headcount
            "vendor_contract": 25000
        }
        self._initialize_permissions()
    
    def _initialize_permissions(self):
        """Set up default permissions for all agents."""
        self._agent_permissions = {
            "ceo_orchestrator": {
                "level": PermissionLevel.APPROVE,
                "can_approve": ["budget", "hiring", "policy_change", "strategy"],
                "spending_limit": float('inf')
            },
            "sales_agent": {
                "level": PermissionLevel.ACT,
                "can_approve": ["discount_under_10_percent"],
                "spending_limit": 25000,
                "hiring_limit": 2
            },
            "marketing_agent": {
                "level": PermissionLevel.ACT,
                "can_approve": ["campaign_under_budget"],
                "spending_limit": 100000,
                "hiring_limit": 1
            },
            "finance_agent": {
                "level": PermissionLevel.RECOMMEND,
                "can_approve": ["budget_reallocation_under_50k"],
                "spending_limit": 0,
                "hiring_limit": 0
            },
            "operations_agent": {
                "level": PermissionLevel.ACT,
                "can_approve": ["vendor_under_25k"],
                "spending_limit": 25000,
                "hiring_limit": 5
            },
            "support_agent": {
                "level": PermissionLevel.RECOMMEND,
                "can_approve": ["refund_under_500"],
                "spending_limit": 500,
                "hiring_limit": 0
            },
            "hr_agent": {
                "level": PermissionLevel.ACT,
                "can_approve": ["job_posting", "interview_process"],
                "spending_limit": 0,
                "hiring_limit": 0  # Can process hiring, not approve headcount
            }
        }
    
    def check_permission(self, agent: str, action: str, 
                         amount: Optional[float] = None) -> Dict[str, Any]:
        """
        Check if an agent has permission for an action.
        
        Returns:
            Dict with allowed (bool), requires_approval (bool), approver (str)
        """
        perms = self._agent_permissions.get(agent, {})
        level = perms.get("level", PermissionLevel.READ)
        
        # Check spending limit
        if amount and amount > perms.get("spending_limit", 0):
            return {
                "allowed": False,
                "requires_approval": True,
                "approver": "ceo_orchestrator",
                "reason": f"Amount ${amount:,.0f} exceeds agent spending limit"
            }
        
        # Check if action type is in can_approve list
        can_approve = perms.get("can_approve", [])
        
        # Map action types
        action_mapping = {
            "budget_request": "budget",
            "hiring_request": "hiring",
            "vendor_contract": "vendor_contract",
            "campaign_launch": "campaign_under_budget",
            "discount": "discount_under_10_percent",
            "refund": "refund_under_500"
        }
        
        required_permission = action_mapping.get(action, action)
        
        if required_permission in can_approve:
            # Check auto-approval thresholds
            auto_limit = self._auto_approval_limits.get(action_mapping.get(action, action), 0)
            if amount and amount <= auto_limit:
                return {
                    "allowed": True,
                    "requires_approval": False,
                    "auto_approved": True,
                    "reason": f"Under auto-approval threshold of ${auto_limit:,.0f}"
                }
            
            return {
                "allowed": True,
                "requires_approval": False,
                "reason": "Agent has authority"
            }
        
        # Needs approval
        return {
            "allowed": False,
            "requires_approval": True,
            "approver": "ceo_orchestrator",
            "reason": f"Agent does not have {required_permission} permission"
        }
    
    def request_approval(self, requester: str, request_type: str,
                        description: str, amount: Optional[float] = None,
                        details: Dict[str, Any] = None) -> ApprovalRequest:
        """
        Create an approval request.
        
        Returns:
            ApprovalRequest with status
        """
        request_id = f"REQ-{len(self._approval_requests) + 1:04d}"
        
        # Check auto-approval
        auto_limit = self._auto_approval_limits.get(request_type, 0)
        if amount and amount <= auto_limit:
            req = ApprovalRequest(
                request_id=request_id,
                requester=requester,
                approver="system",
                request_type=request_type,
                description=description,
                amount=amount,
                details=details,
                status=ApprovalStatus.AUTO_APPROVED
            )
            self._approval_requests.append(req)
            return req
        
        # Requires manual approval
        req = ApprovalRequest(
            request_id=request_id,
            requester=requester,
            approver="ceo_orchestrator",
            request_type=request_type,
            description=description,
            amount=amount,
            details=details,
            status=ApprovalStatus.PENDING
        )
        self._approval_requests.append(req)
        return req
    
    def approve(self, request_id: str, approver: str, 
                conditions: List[str] = None) -> Optional[ApprovalRequest]:
        """Approve a pending request."""
        for req in self._approval_requests:
            if req.request_id == request_id:
                req.status = ApprovalStatus.APPROVED
                req.approver = approver
                if conditions:
                    req.conditions.extend(conditions)
                return req
        return None
    
    def reject(self, request_id: str, approver: str, reason: str) -> Optional[ApprovalRequest]:
        """Reject a pending request."""
        for req in self._approval_requests:
            if req.request_id == request_id:
                req.status = ApprovalStatus.REJECTED
                req.approver = approver
                req.details["rejection_reason"] = reason
                return req
        return None
    
    def escalate(self, request_id: str, reason: str) -> Optional[ApprovalRequest]:
        """Escalate a request to CEO."""
        for req in self._approval_requests:
            if req.request_id == request_id:
                req.status = ApprovalStatus.ESCALATED
                req.details["escalation_reason"] = reason
                req.approver = "ceo"
                return req
        return None
    
    def get_pending_requests(self) -> List[ApprovalRequest]:
        """Get all pending approval requests."""
        return [r for r in self._approval_requests if r.status == ApprovalStatus.PENDING]
    
    def get_approval_summary(self) -> Dict[str, Any]:
        """Get summary of all approval requests."""
        by_status = {}
        for req in self._approval_requests:
            status = req.status.value
            by_status[status] = by_status.get(status, 0) + 1
        
        return {
            "total_requests": len(self._approval_requests),
            "by_status": by_status,
            "pending": len(self.get_pending_requests()),
            "auto_approved": by_status.get("auto_approved", 0)
        }
    
    def should_escalate(self, agent_output: Dict[str, Any]) -> Tuple[bool, str]:
        """
        Determine if an agent output should be escalated to CEO.
        
        Returns:
            Tuple of (should_escalate, reason)
        """
        # Escalation rules
        
        # 1. Low confidence recommendations
        if agent_output.get("confidence", 1.0) < 0.6:
            return True, "Confidence below threshold (60%)"
        
        # 2. High budget impact
        if agent_output.get("budget_impact", 0) > 500000:
            return True, "Budget impact exceeds $500K"
        
        # 3. Strategic policy changes
        if agent_output.get("requires_policy_change", False):
            return True, "Requires policy change"
        
        # 4. High headcount impact
        if agent_output.get("headcount_impact", 0) > 20:
            return True, "Headcount impact exceeds 20 FTE"
        
        # 5. Cross-department impact
        if len(agent_output.get("affected_departments", [])) > 3:
            return True, "Affects more than 3 departments"
        
        return False, ""
