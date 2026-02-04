"""
HR Agent

Handles hiring plans, workforce strategy, performance systems, and compliance support.
"""

from typing import Dict, List, Any
from .base_agent import BaseAgent, AgentOutput


class HRAgent(BaseAgent):
    """
    Human Resources functional agent for the insurance enterprise.
    
    Responsibilities:
    - Hiring plans and recruitment strategy
    - Workforce planning and strategy
    - Performance management systems
    - Compliance and regulatory support
    """
    
    def __init__(self):
        super().__init__("hr_agent")
    
    def process_task(self, task: Dict[str, Any], 
                     shared_memory: Any,
                     enterprise_data: Any,
                     audit_logger: Any) -> AgentOutput:
        """
        Process HR-related tasks.
        
        Task types:
        - "hiring_plan": Develop hiring plans
        - "workforce_strategy": Workforce planning
        - "performance_systems": Performance management
        - "compliance": Compliance support
        """
        task_type = task.get("type", "general")
        task_id = self._generate_task_id()
        
        # Access HR data
        hr = enterprise_data.hr
        
        headcount_summary = hr.get_headcount_summary()
        
        citation1 = self._access_data(
            audit_logger, "HRIS", "headcount_analysis",
            headcount_summary["total_current"], "workforce planning"
        )
        
        citations = [citation1]
        
        if task_type == "hiring_plan":
            return self._handle_hiring_plan(
                task, task_id, headcount_summary, hr, citations
            )
        elif task_type == "workforce_strategy":
            return self._handle_workforce_strategy(task, task_id, headcount_summary, citations)
        elif task_type == "performance_systems":
            return self._handle_performance_systems(task, task_id, citations)
        else:
            return self._handle_general_task(task, task_id, citations)
    
    def _handle_hiring_plan(self, task: Dict[str, Any], task_id: str,
                           headcount_summary: Dict, hr: Any, citations: List[str]) -> AgentOutput:
        """Handle hiring plan for retention initiative."""
        
        # Calculate hiring needs based on other agents' requirements
        # Sales: 8 CSMs, Support: 6 specialists, Operations: 0 (automation)
        
        hiring_needs = [
            {"role": "Customer Success Manager", "count": 8, "dept": "sales", "salary": 90000},
            {"role": "Support Specialist", "count": 6, "dept": "support", "salary": 55000},
            {"role": "Claims Processor", "count": 4, "dept": "operations", "salary": 52000},
            {"role": "Data Analyst", "count": 2, "dept": "operations", "salary": 85000}
        ]
        
        total_new_hires = sum(h["count"] for h in hiring_needs)
        total_cost = sum(h["count"] * h["salary"] for h in hiring_needs)
        
        # Check capacity
        capacity_check = hr.check_hiring_capacity("sales", 8)
        
        recommendations = [
            self._format_recommendation(
                title=f"Retention Initiative Hiring Plan: {total_new_hires} FTE",
                description=f"Strategic hiring to support 8% retention improvement goal",
                expected_impact=f"Enable retention programs across customer-facing teams",
                action_items=[
                    f"Hire {hiring_needs[0]['count']} Customer Success Managers (${hiring_needs[0]['salary']:,} avg)",
                    f"Hire {hiring_needs[1]['count']} Support Specialists (${hiring_needs[1]['salary']:,} avg)",
                    f"Hire {hiring_needs[2]['count']} Claims Processors (${hiring_needs[2]['salary']:,} avg)",
                    f"Hire {hiring_needs[3]['count']} Data Analysts (${hiring_needs[3]['salary']:,} avg)",
                    "Launch referral bonus program to accelerate sourcing",
                    "Partner with 3 recruitment agencies for specialized roles",
                    "Implement structured interview process for consistency"
                ]
            ),
            self._format_recommendation(
                title="Talent Acquisition Strategy",
                description="Multi-channel sourcing strategy to fill roles in 60-75 days",
                expected_impact="Reduce time-to-fill by 20%, improve quality of hire",
                action_items=[
                    "Post on insurance industry job boards",
                    "Activate employee referral program (>$2K bonus)",
                    "Source from competitor talent pools",
                    "Partner with universities for entry-level pipeline",
                    "Implement pre-employment assessments"
                ]
            ),
            self._format_recommendation(
                title="Onboarding Excellence Program",
                description="Structured 90-day onboarding to ensure new hire success",
                expected_impact="85% new hire retention at 1 year, faster time-to-productivity",
                action_items=[
                    "Create role-specific onboarding tracks",
                    "Assign onboarding buddies for each new hire",
                    "Implement 30-60-90 day check-ins",
                    "Build new hire feedback loop for continuous improvement"
                ]
            ),
            self._format_recommendation(
                title="Compliance & Risk Management",
                description="Ensure all hiring meets regulatory requirements",
                expected_impact="100% compliance with insurance industry regulations",
                action_items=[
                    "Background checks for all customer-facing roles",
                    "Verify insurance licenses where required",
                    "Document hiring decisions for audit trail",
                    "Train hiring managers on compliance requirements"
                ]
            )
        ]
        
        # Calculate timeline
        timeline_by_role = []
        for need in hiring_needs:
            timeline = hr.estimate_hiring_timeline(need["dept"], need["count"])
            timeline_by_role.append({
                "role": need["role"],
                "timeline_days": timeline["estimated_days"]
            })
        
        max_timeline = max(t["timeline_days"] for t in timeline_by_role)
        
        confidence = self._assess_confidence(
            data_quality=0.85,
            assumptions_made=2,
            historical_precedent=True
        )
        
        return AgentOutput(
            agent_name=self.agent_name,
            task_id=task_id,
            recommendations=recommendations,
            confidence=confidence,
            what_would_change_mind=[
                "Market data shows significantly different salary expectations",
                "Talent availability much lower than forecasted",
                "Budget constraints require >30% reduction in hiring",
                "Regulatory changes affect licensing requirements"
            ],
            citations=citations,
            budget_impact=total_cost * 1.25,  # Including benefits
            headcount_impact=total_new_hires,
            timeline_days=max_timeline,
            risks=[
                "Competitive talent market may extend hiring timelines",
                "Salary expectations may exceed budgeted amounts",
                "New hire quality may vary affecting program success",
                "Regulatory licensing delays for insurance roles"
            ],
            dependencies=[
                "Budget approval for headcount",
                "Hiring manager availability for interviews",
                "ATS system configuration for new requisitions",
                "Compliance review of job descriptions"
            ]
        )
    
    def _handle_workforce_strategy(self, task: Dict[str, Any], task_id: str,
                                   headcount_summary: Dict, citations: List[str]) -> AgentOutput:
        """Handle workforce strategy."""
        
        current = headcount_summary["total_current"]
        target = headcount_summary["total_target"]
        
        recommendations = [
            self._format_recommendation(
                title="Flexible Workforce Model",
                description=f"Balance FTE ({current}) with contractors for peak periods",
                expected_impact="20% improvement in workforce flexibility, cost optimization",
                action_items=[
                    "Identify roles suitable for contracting",
                    "Build contractor talent pool",
                    "Implement seasonal staffing model",
                    "Create conversion pathway for top contractors"
                ]
            )
        ]
        
        return AgentOutput(
            agent_name=self.agent_name,
            task_id=task_id,
            recommendations=recommendations,
            confidence=0.75,
            what_would_change_mind=["Strategic direction shifts to in-house only model"],
            citations=citations,
            budget_impact=0,
            timeline_days=90
        )
    
    def _handle_performance_systems(self, task: Dict[str, Any], task_id: str,
                                   citations: List[str]) -> AgentOutput:
        """Handle performance management systems."""
        
        recommendations = [
            self._format_recommendation(
                title="Retention-Linked Performance Metrics",
                description="Align team goals with company retention objectives",
                expected_impact="Improved accountability for retention across teams",
                action_items=[
                    "Add retention metrics to CS team goals",
                    "Include customer satisfaction in performance reviews",
                    "Create team-based retention incentives",
                    "Implement monthly retention scorecards"
                ]
            )
        ]
        
        return AgentOutput(
            agent_name=self.agent_name,
            task_id=task_id,
            recommendations=recommendations,
            confidence=0.80,
            what_would_change_mind=["Performance system recently redesigned"],
            citations=citations,
            budget_impact=25_000,
            timeline_days=30
        )
    
    def _handle_general_task(self, task: Dict[str, Any], task_id: str,
                            citations: List[str]) -> AgentOutput:
        """Handle general HR tasks."""
        
        return AgentOutput(
            agent_name=self.agent_name,
            task_id=task_id,
            recommendations=[],
            confidence=0.5,
            what_would_change_mind=["More specific task requirements provided"],
            citations=citations
        )
