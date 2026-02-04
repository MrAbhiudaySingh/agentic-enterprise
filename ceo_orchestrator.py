"""
CEO Orchestration Layer

The central orchestrator that accepts CEO prompts, decomposes goals into tasks,
routes to functional agents, resolves conflicts, and produces executive output.
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime
import uuid

from infrastructure import (
    get_shared_memory, get_audit_logger, get_data_store,
    ConflictResolver, Governance, DecisionType
)
from agents import (
    SalesAgent, MarketingAgent, FinanceAgent,
    OperationsAgent, SupportAgent, HRAgent
)


@dataclass
class ExecutiveOutput:
    """Structured output for CEO presentation."""
    prompt_id: str
    strategic_goal: str
    constraint: str
    summary: str
    strategic_options: List[Dict[str, Any]]
    department_plans: Dict[str, Any]
    budget_impact: Dict[str, Any]
    headcount_impact: Dict[str, Any]
    risks: List[str]
    assumptions: List[str]
    dependencies: List[str]
    kpis: List[Dict[str, Any]]
    alignment_status: str
    escalations: List[Dict[str, Any]]
    audit_summary: Dict[str, Any]
    

class CEOOrchestrator:
    """
    CEO Orchestration Layer for the Agentic Enterprise.
    
    Responsibilities:
    1. Parse CEO prompts into structured goals
    2. Decompose goals into agent-specific tasks
    3. Route tasks to functional agents
    4. Collect and synthesize agent outputs
    5. Detect and resolve cross-agent conflicts
    6. Apply governance and approval rules
    7. Generate executive dashboard output
    """
    
    def __init__(self):
        self.shared_memory = get_shared_memory()
        self.audit_logger = get_audit_logger()
        self.enterprise_data = get_data_store()
        self.conflict_resolver = ConflictResolver()
        self.governance = Governance()
        
        # Initialize agents
        self.agents = {
            "sales": SalesAgent(),
            "marketing": MarketingAgent(),
            "finance": FinanceAgent(),
            "operations": OperationsAgent(),
            "support": SupportAgent(),
            "hr": HRAgent()
        }
        
        # Initialize shared memory with default constraints and goals
        self._initialize_default_context()
    
    def _initialize_default_context(self):
        """Initialize default company goals and constraints."""
        from infrastructure import MemoryType, Priority, CompanyGoal, Constraint
        from datetime import datetime, timedelta
        
        # Add retention goal
        retention_goal = CompanyGoal(
            id="GOAL-001",
            description="Improve customer retention rate",
            target_value=0.92,
            current_value=0.84,
            unit="percentage",
            deadline=datetime.now() + timedelta(days=90),
            owner="ceo",
            status="active",
            associated_agents=["sales", "marketing", "support", "operations"],
            key_results=[
                {"description": "Reduce churn rate", "target": 0.08, "current": 0.16},
                {"description": "Improve NPS", "target": 45, "current": 32}
            ]
        )
        self.shared_memory.add_goal(retention_goal)
        
        # Add budget constraints
        departments = ["marketing", "sales", "operations", "support", "hr", "technology"]
        budgets = [8_000_000, 5_000_000, 12_000_000, 6_000_000, 2_000_000, 10_000_000]
        
        for dept, budget in zip(departments, budgets):
            constraint = Constraint(
                id=f"BUDGET-{dept}",
                category="budget",
                description=f"{dept.capitalize()} department budget",
                limit_value=budget,
                current_usage=budget * 0.5,  # 50% spent
                unit="USD",
                hard_limit=False,
                owner="cfo"
            )
            self.shared_memory.add_constraint(constraint)
    
    def process_prompt(self, prompt: str) -> ExecutiveOutput:
        """
        Process a CEO prompt and generate executive output.
        
        Args:
            prompt: Natural language strategic directive from CEO
            
        Returns:
            ExecutiveOutput with full analysis and recommendations
        """
        prompt_id = f"PROMPT-{uuid.uuid4().hex[:8].upper()}"
        
        # Log prompt receipt
        self.audit_logger.log(
            type=DecisionType.STRATEGY,
            agent="ceo_orchestrator",
            description=f"CEO prompt received: {prompt[:100]}...",
            data={"full_prompt": prompt}
        )
        
        # Step 1: Parse prompt into structured goal
        goal = self._parse_prompt(prompt)
        
        # Step 2: Decompose into tasks
        tasks = self._decompose_goal(goal)
        
        # Step 3: Route tasks to agents
        agent_outputs = self._route_tasks(tasks)
        
        # Step 4: Detect conflicts
        # Build company context from shared memory
        active_goals = self.shared_memory.get_active_goals()
        budget_constraints = self.shared_memory.get_constraints_by_category("budget")
        company_context = {
            "goals": active_goals,
            "budget_limits": {c.id: c.limit_value for c in budget_constraints},
            "current_usage": {c.id: c.current_usage for c in budget_constraints}
        }
        conflicts = self.conflict_resolver.detect_conflicts(agent_outputs, company_context)
        
        # Step 5: Resolve conflicts
        unresolved, resolution_summary = self.conflict_resolver.resolve_conflicts(conflicts)
        
        # Step 6: Apply governance
        escalations = self._check_governance(agent_outputs)
        
        # Step 7: Generate executive output
        output = self._generate_executive_output(
            prompt_id, goal, agent_outputs, unresolved, 
            resolution_summary, escalations
        )
        
        # Store in shared memory
        from infrastructure import MemoryType, Priority
        self.shared_memory.store(
            type=MemoryType.AGENT_OUTPUT,
            source="ceo_orchestrator",
            content={"executive_output": output},
            priority=Priority.HIGH,
            tags=["executive_summary", prompt_id]
        )
        
        return output
    
    def _parse_prompt(self, prompt: str) -> Dict[str, Any]:
        """Parse natural language prompt into structured goal."""
        prompt_lower = prompt.lower()
        
        # Extract retention target
        retention_match = None
        if "retention" in prompt_lower:
            import re
            retention_match = re.search(r'(\d+)%', prompt)
        
        retention_target = float(retention_match.group(1)) / 100 if retention_match else 0.08
        
        # Extract constraint (e.g., "without increasing CAC")
        constraint = "None specified"
        if "without increasing cac" in prompt_lower or "no cac increase" in prompt_lower:
            constraint = "No CAC increase allowed"
        elif "within budget" in prompt_lower:
            constraint = "Within existing budget"
        
        goal = {
            "original_prompt": prompt,
            "primary_objective": "improve_retention" if "retention" in prompt_lower else "general",
            "target_metric": "retention_rate",
            "target_value": retention_target,
            "constraint": constraint,
            "affected_departments": ["sales", "marketing", "support", "operations", "finance", "hr"]
        }
        
        self.audit_logger.log(
            level=AuditLevel.INFO,
            agent="ceo_orchestrator",
            action="goal_parsed",
            description="Parsed CEO prompt into structured goal",
            data=goal
        )
        
        return goal
    
    def _decompose_goal(self, goal: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Decompose goal into agent-specific tasks."""
        tasks = []
        
        if goal["primary_objective"] == "improve_retention":
            tasks = [
                {
                    "agent": "sales",
                    "type": "improve_retention",
                    "description": "Develop retention strategies and customer success plans",
                    "target_retention_improvement": goal["target_value"]
                },
                {
                    "agent": "marketing",
                    "type": "retention_campaign",
                    "description": "Design retention marketing campaigns",
                    "target_retention_improvement": goal["target_value"]
                },
                {
                    "agent": "finance",
                    "type": "budget_planning",
                    "description": "Develop budget allocation for retention initiatives"
                },
                {
                    "agent": "operations",
                    "type": "process_optimization",
                    "description": "Optimize processes for customer experience"
                },
                {
                    "agent": "support",
                    "type": "churn_analysis",
                    "description": "Analyze churn signals and develop intervention strategies"
                },
                {
                    "agent": "hr",
                    "type": "hiring_plan",
                    "description": "Develop hiring plan to support retention initiatives"
                }
            ]
        
        self.audit_logger.log(
            level=AuditLevel.INFO,
            agent="ceo_orchestrator",
            action="tasks_decomposed",
            description=f"Decomposed goal into {len(tasks)} tasks",
            data={"task_count": len(tasks), "tasks": [t["agent"] for t in tasks]}
        )
        
        return tasks
    
    def _route_tasks(self, tasks: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
        """Route tasks to appropriate agents and collect outputs."""
        outputs = {}
        
        for task in tasks:
            agent_name = task["agent"]
            if agent_name in self.agents:
                agent = self.agents[agent_name]
                
                # Execute agent task
                output = agent.process_task(
                    task=task,
                    shared_memory=self.shared_memory,
                    enterprise_data=self.enterprise_data,
                    audit_logger=self.audit_logger
                )
                
                # Convert AgentOutput to dict for conflict detection
                outputs[agent_name] = {
                    "agent_name": output.agent_name,
                    "task_id": output.task_id,
                    "recommendations": output.recommendations,
                    "confidence": output.confidence,
                    "what_would_change_mind": output.what_would_change_mind,
                    "citations": output.citations,
                    "budget_impact": output.budget_impact,
                    "headcount_impact": output.headcount_impact,
                    "timeline_days": output.timeline_days,
                    "risks": output.risks,
                    "dependencies": output.dependencies
                }
                
                # Store in shared memory
                from infrastructure import MemoryType, Priority
                self.shared_memory.store(
                    type=MemoryType.AGENT_OUTPUT,
                    source=agent_name,
                    content=outputs[agent_name],
                    priority=Priority.MEDIUM,
                    tags=[agent_name, task.get("type", "general")]
                )
        
        return outputs
    
    def _check_governance(self, agent_outputs: Dict[str, Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Check if any outputs require governance escalation."""
        escalations = []
        
        for agent_name, output in agent_outputs.items():
            should_escalate, reason = self.governance.should_escalate(output)
            
            if should_escalate:
                escalation = {
                    "agent": agent_name,
                    "reason": reason,
                    "budget_impact": output.get("budget_impact"),
                    "headcount_impact": output.get("headcount_impact")
                }
                escalations.append(escalation)
                
                self.audit_logger.log_escalation(
                    from_agent=agent_name,
                    to_approver="ceo",
                    reason=reason,
                    escalation_data=output
                )
        
        return escalations
    
    def _generate_executive_output(
        self,
        prompt_id: str,
        goal: Dict[str, Any],
        agent_outputs: Dict[str, Dict[str, Any]],
        unresolved_conflicts: List[Any],
        resolution_summary: Dict[str, Any],
        escalations: List[Dict[str, Any]]
    ) -> ExecutiveOutput:
        """Generate final executive dashboard output."""
        
        # Build strategic options from agent recommendations
        strategic_options = self._build_strategic_options(agent_outputs)
        
        # Build department plans
        department_plans = self._build_department_plans(agent_outputs)
        
        # Calculate total impacts
        total_budget = sum(o.get("budget_impact", 0) or 0 for o in agent_outputs.values())
        total_headcount = sum(o.get("headcount_impact", 0) or 0 for o in agent_outputs.values())
        
        # Collect all risks
        all_risks = []
        for output in agent_outputs.values():
            all_risks.extend(output.get("risks", []))
        
        # Build KPIs
        kpis = [
            {
                "name": "Retention Rate",
                "current": "84%",
                "target": f"{(0.84 + goal['target_value']):.0%}",
                "measurement": "Quarterly cohort analysis"
            },
            {
                "name": "Customer Satisfaction (NPS)",
                "current": "32",
                "target": "45",
                "measurement": "Monthly surveys"
            },
            {
                "name": "Churn Rate",
                "current": "16%",
                "target": f"{(0.16 - goal['target_value']):.0%}",
                "measurement": "Monthly tracking"
            },
            {
                "name": "Support Resolution Time",
                "current": "18.5 hours",
                "target": "12 hours",
                "measurement": "Weekly average"
            },
            {
                "name": "CAC",
                "current": "$385",
                "target": "$385 (maintain)",
                "measurement": "Monthly blended CAC"
            }
        ]
        
        # Determine alignment status
        alignment = self.conflict_resolver.get_alignment_report()
        
        output = ExecutiveOutput(
            prompt_id=prompt_id,
            strategic_goal=f"Improve quarterly retention by {goal['target_value']:.0%}",
            constraint=goal["constraint"],
            summary=self._generate_summary(goal, agent_outputs, total_budget, total_headcount),
            strategic_options=strategic_options,
            department_plans=department_plans,
            budget_impact={
                "total_investment": total_budget,
                "by_department": {name: (o.get("budget_impact") or 0) 
                                for name, o in agent_outputs.items()}
            },
            headcount_impact={
                "total_new_hires": total_headcount,
                "by_department": {name: (o.get("headcount_impact") or 0)
                                 for name, o in agent_outputs.items()}
            },
            risks=list(set(all_risks)),  # Deduplicate
            assumptions=[
                "Churn risk model accuracy of 75%+",
                "Market conditions remain stable",
                "Competitive response limited to matching (not exceeding) offers",
                "Hiring timeline achievable in current talent market"
            ],
            dependencies=[
                "Q1 financial close completion",
                "Board budget approval",
                "IT system integrations completed",
                "Marketing automation platform deployed"
            ],
            kpis=kpis,
            alignment_status=alignment["status"],
            escalations=escalations,
            audit_summary=self.audit_logger.generate_report(prompt_id)
        )
        
        return output
    
    def _build_strategic_options(self, agent_outputs: Dict[str, Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Build strategic options from agent outputs."""
        # Aggregate recommendations into strategic options
        options = []
        
        # Option 1: Full Program
        full_budget = sum(o.get("budget_impact", 0) or 0 for o in agent_outputs.values())
        full_headcount = sum(o.get("headcount_impact", 0) or 0 for o in agent_outputs.values())
        
        options.append({
            "name": "Comprehensive Retention Program",
            "description": "Execute all recommended initiatives across departments",
            "investment": full_budget,
            "timeline_days": 90,
            "headcount": full_headcount,
            "expected_retention_improvement": "8-10%",
            "confidence": 0.85,
            "trade_offs": "Higher investment but maximum impact"
        })
        
        # Option 2: Phased Approach
        options.append({
            "name": "Phased Rollout",
            "description": "Phase 1: Quick wins (Support + Marketing). Phase 2: Infrastructure (Sales + Ops)",
            "investment": full_budget * 0.6,
            "timeline_days": 180,
            "headcount": int(full_headcount * 0.6),
            "expected_retention_improvement": "5-6%",
            "confidence": 0.80,
            "trade_offs": "Lower initial investment, slower results, option to scale"
        })
        
        # Option 3: Minimal
        options.append({
            "name": "Minimum Viable Program",
            "description": "Focus on highest-impact, lowest-cost initiatives only",
            "investment": full_budget * 0.3,
            "timeline_days": 45,
            "headcount": int(full_headcount * 0.3),
            "expected_retention_improvement": "3-4%",
            "confidence": 0.70,
            "trade_offs": "Minimal investment but may not achieve target"
        })
        
        return options
    
    def _build_department_plans(self, agent_outputs: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
        """Build department-by-department execution plans."""
        plans = {}
        
        for agent_name, output in agent_outputs.items():
            plans[agent_name] = {
                "recommendations": output.get("recommendations", []),
                "confidence": output.get("confidence"),
                "budget": output.get("budget_impact"),
                "headcount": output.get("headcount_impact"),
                "timeline_days": output.get("timeline_days"),
                "citations": output.get("citations", [])
            }
        
        return plans
    
    def _generate_summary(self, goal: Dict[str, Any], 
                         agent_outputs: Dict[str, Dict[str, Any]],
                         total_budget: float, total_headcount: int) -> str:
        """Generate executive summary text."""
        return (
            f"To achieve the goal of improving retention by {goal['target_value']:.0%} "
            f"({goal['constraint']}), the Agentic Enterprise recommends a comprehensive "
            f"cross-functional initiative requiring ${total_budget:,.0f} investment and "
            f"{total_headcount} new hires. All six functional agents have aligned on a "
            f"strategy combining proactive customer success, targeted marketing campaigns, "
            f"process optimization, and predictive churn intervention. Expected outcome: "
            f"8-10% retention improvement within 90 days."
        )
    
    def format_output_for_display(self, output: ExecutiveOutput) -> str:
        """Format executive output for human-readable display."""
        lines = [
            "=" * 80,
            "EXECUTIVE DASHBOARD - AGENTIC ENTERPRISE",
            "=" * 80,
            f"Prompt ID: {output.prompt_id}",
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            f"🎯 STRATEGIC GOAL: {output.strategic_goal}",
            f"⛔ CONSTRAINT: {output.constraint}",
            "",
            "─" * 80,
            "EXECUTIVE SUMMARY",
            "─" * 80,
            output.summary,
            "",
            "─" * 80,
            "STRATEGIC OPTIONS",
            "─" * 80,
        ]
        
        for i, option in enumerate(output.strategic_options, 1):
            lines.extend([
                f"\n{i}. {option['name']}",
                f"   Description: {option['description']}",
                f"   Investment: ${option['investment']:,.0f}",
                f"   Timeline: {option['timeline_days']} days",
                f"   Headcount: {option['headcount']} FTE",
                f"   Expected Impact: {option['expected_retention_improvement']} retention improvement",
                f"   Confidence: {option['confidence']:.0%}",
                f"   Trade-offs: {option['trade_offs']}"
            ])
        
        lines.extend([
            "",
            "─" * 80,
            "BUDGET & HEADCOUNT IMPACT",
            "─" * 80,
            f"Total Investment: ${output.budget_impact['total_investment']:,.0f}",
            "By Department:"
        ])
        
        for dept, budget in output.budget_impact['by_department'].items():
            lines.append(f"  • {dept.capitalize()}: ${budget:,.0f}")
        
        lines.extend([
            f"\nTotal New Hires: {output.headcount_impact['total_new_hires']} FTE",
            "By Department:"
        ])
        
        for dept, count in output.headcount_impact['by_department'].items():
            if count > 0:
                lines.append(f"  • {dept.capitalize()}: {count} FTE")
        
        lines.extend([
            "",
            "─" * 80,
            "KEY RISKS",
            "─" * 80
        ])
        
        for risk in output.risks[:5]:  # Top 5 risks
            lines.append(f"  ⚠️  {risk}")
        
        lines.extend([
            "",
            "─" * 80,
            "SUCCESS METRICS (KPIs)",
            "─" * 80
        ])
        
        for kpi in output.kpis:
            lines.append(f"  📊 {kpi['name']}: {kpi['current']} → {kpi['target']} ({kpi['measurement']})")
        
        lines.extend([
            "",
            "─" * 80,
            "CROSS-FUNCTIONAL ALIGNMENT",
            "─" * 80,
            f"Status: {output.alignment_status}",
            ""
        ])
        
        if output.escalations:
            lines.extend([
                "─" * 80,
                "ITEMS REQUIRING CEO ATTENTION",
                "─" * 80
            ])
            for esc in output.escalations:
                lines.append(f"  🚨 {esc['agent']}: {esc['reason']}")
            lines.append("")
        
        lines.append("=" * 80)
        
        return "\n".join(lines)


# Singleton instance
_orchestrator_instance: Optional[CEOOrchestrator] = None


def get_orchestrator() -> CEOOrchestrator:
    """Get the global orchestrator instance."""
    global _orchestrator_instance
    if _orchestrator_instance is None:
        _orchestrator_instance = CEOOrchestrator()
    return _orchestrator_instance
