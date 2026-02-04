"""
Enterprise Data Layer - Mock data for CRM, ERP, Finance, Support, and HRIS systems.

This module provides realistic mock data for an insurance company, ensuring
all agents cite actual data sources rather than hallucinating facts.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import random


@dataclass
class Customer:
    id: str
    name: str
    segment: str  # "enterprise", "smb", "individual"
    policy_type: str  # "life", "health", "auto", "home", "commercial"
    premium: float
    tenure_months: int
    churn_risk_score: float  # 0-1
    satisfaction_score: float  # 1-10
    last_contact: datetime
    renewal_date: datetime
    claims_count: int
    claims_value: float
    acquisition_channel: str
    cac: float  # Customer Acquisition Cost


@dataclass
class Policy:
    id: str
    name: str
    type: str
    base_premium: float
    loss_ratio: float  # claims paid / premiums earned
    retention_rate: float
    growth_rate: float
    active_policies: int
    revenue_annual: float


@dataclass
class SalesOpportunity:
    id: str
    customer_id: str
    policy_type: str
    estimated_value: float
    stage: str  # "prospect", "qualified", "proposal", "negotiation", "closed_won", "closed_lost"
    probability: float
    created_date: datetime
    expected_close: datetime
    assigned_rep: str
    source: str


@dataclass
class MarketingCampaign:
    id: str
    name: str
    channel: str  # "digital", "email", "events", "partnerships", "direct"
    budget: float
    spent: float
    leads_generated: int
    opportunities_created: int
    policies_sold: int
    revenue_attributed: float
    start_date: datetime
    end_date: datetime
    status: str


@dataclass
class SupportTicket:
    id: str
    customer_id: str
    category: str  # "claim", "billing", "policy", "technical", "complaint"
    priority: str  # "low", "medium", "high", "critical"
    status: str  # "open", "in_progress", "resolved", "closed"
    created_at: datetime
    resolved_at: Optional[datetime]
    satisfaction_rating: Optional[float]
    churn_risk_flag: bool


@dataclass
class Employee:
    id: str
    name: str
    department: str
    role: str
    level: str  # "entry", "mid", "senior", "lead", "executive"
    salary: float
    hire_date: datetime
    performance_rating: float  # 1-5
    utilization_rate: float  # 0-1
    cost_center: str


@dataclass
class FinancialMetrics:
    period: str
    revenue: float
    cogs: float  # Claims paid
    gross_profit: float
    opex: float
    ebitda: float
    cash_flow: float
    loss_ratio: float
    combined_ratio: float
    cac: float
    ltv: float
    ltv_cac_ratio: float
    retention_rate: float


class EnterpriseDataStore:
    """
    Central mock data store for all enterprise systems.
    Provides realistic insurance company data for Q3 2024.
    """
    
    def __init__(self):
        self.customers: Dict[str, Customer] = {}
        self.policies: Dict[str, Policy] = {}
        self.opportunities: Dict[str, SalesOpportunity] = {}
        self.campaigns: Dict[str, MarketingCampaign] = {}
        self.tickets: Dict[str, SupportTicket] = {}
        self.employees: Dict[str, Employee] = {}
        self.financial_history: List[FinancialMetrics] = []
        
        self._initialize_data()
    
    def _initialize_data(self):
        """Initialize realistic mock data for an insurance company."""
        
        # Policy Portfolio
        policies_data = [
            Policy("POL-LIFE-001", "Term Life Plus", "life", 1200, 0.65, 0.88, 0.03, 45000, 54000000),
            Policy("POL-HEALTH-001", "Premium Health Shield", "health", 3600, 0.72, 0.82, 0.05, 32000, 115200000),
            Policy("POL-AUTO-001", "Complete Auto Coverage", "auto", 1800, 0.68, 0.85, 0.02, 58000, 104400000),
            Policy("POL-HOME-001", "Homeowner's Protect", "home", 2400, 0.55, 0.90, 0.04, 41000, 98400000),
            Policy("POL-COMM-001", "Business Comprehensive", "commercial", 8500, 0.58, 0.92, 0.06, 8500, 72250000),
        ]
        for policy in policies_data:
            self.policies[policy.id] = policy
        
        # Generate Customers
        segments = ["enterprise", "smb", "individual"]
        policy_types = ["life", "health", "auto", "home", "commercial"]
        channels = ["digital", "agent", "referral", "partnership", "direct_mail"]
        
        random.seed(42)  # Reproducible data
        for i in range(1000):
            segment = random.choice(segments)
            policy_type = random.choice(policy_types)
            
            # Adjust premiums by segment
            base_premium = {"life": 1200, "health": 3600, "auto": 1800, "home": 2400, "commercial": 8500}[policy_type]
            if segment == "enterprise":
                base_premium *= 5
            elif segment == "smb":
                base_premium *= 2
            
            # Calculate churn risk based on factors
            tenure = random.randint(1, 120)
            satisfaction = random.uniform(6.5, 9.5)
            claims = random.randint(0, 5)
            churn_risk = max(0, min(1, (1 - satisfaction/10) * 0.4 + (claims / 10) * 0.3 + random.uniform(-0.1, 0.1)))
            
            customer = Customer(
                id=f"CUST-{i+1:05d}",
                name=f"Customer {i+1}",
                segment=segment,
                policy_type=policy_type,
                premium=base_premium * random.uniform(0.9, 1.3),
                tenure_months=tenure,
                churn_risk_score=churn_risk,
                satisfaction_score=satisfaction,
                last_contact=datetime.now() - timedelta(days=random.randint(1, 90)),
                renewal_date=datetime.now() + timedelta(days=random.randint(30, 365)),
                claims_count=claims,
                claims_value=claims * random.uniform(2000, 15000),
                acquisition_channel=random.choice(channels),
                cac=random.uniform(200, 1500) if segment == "individual" else random.uniform(1000, 5000)
            )
            self.customers[customer.id] = customer
        
        # Sales Opportunities
        stages = ["prospect", "qualified", "proposal", "negotiation", "closed_won", "closed_lost"]
        stage_probs = {"prospect": 0.1, "qualified": 0.25, "proposal": 0.4, "negotiation": 0.6, "closed_won": 1.0, "closed_lost": 0.0}
        
        reps = ["Alice Chen", "Bob Martinez", "Carol Williams", "David Park", "Emma Thompson"]
        
        for i in range(250):
            stage = random.choice(stages)
            opp = SalesOpportunity(
                id=f"OPP-{i+1:05d}",
                customer_id=f"CUST-{random.randint(1, 1000):05d}",
                policy_type=random.choice(policy_types),
                estimated_value=random.uniform(5000, 50000),
                stage=stage,
                probability=stage_probs[stage],
                created_date=datetime.now() - timedelta(days=random.randint(1, 180)),
                expected_close=datetime.now() + timedelta(days=random.randint(1, 90)),
                assigned_rep=random.choice(reps),
                source=random.choice(["website", "referral", "event", "cold_call", "partner"])
            )
            self.opportunities[opp.id] = opp
        
        # Marketing Campaigns
        campaigns_data = [
            ("Summer Retention Drive", "email", 150000, 120000, 4500, 320, 180, 850000),
            ("Digital Acquisition Q3", "digital", 300000, 280000, 8200, 650, 340, 1850000),
            ("Agent Network Expansion", "partnerships", 200000, 180000, 1200, 480, 290, 1450000),
            ("SMB Roadshow Series", "events", 120000, 95000, 800, 280, 165, 920000),
            ("Direct Mail Renewal", "direct", 80000, 78000, 3200, 180, 125, 520000),
        ]
        
        for i, (name, channel, budget, spent, leads, opps, sales, revenue) in enumerate(campaigns_data):
            campaign = MarketingCampaign(
                id=f"CAMP-{i+1:03d}",
                name=name,
                channel=channel,
                budget=budget,
                spent=spent,
                leads_generated=leads,
                opportunities_created=opps,
                policies_sold=sales,
                revenue_attributed=revenue,
                start_date=datetime.now() - timedelta(days=random.randint(30, 90)),
                end_date=datetime.now() + timedelta(days=random.randint(1, 60)),
                status="active" if i < 3 else "completed"
            )
            self.campaigns[campaign.id] = campaign
        
        # Support Tickets
        categories = ["claim", "billing", "policy", "technical", "complaint"]
        priorities = ["low", "medium", "high", "critical"]
        
        for i in range(500):
            created = datetime.now() - timedelta(days=random.randint(1, 60))
            resolved = None if random.random() < 0.2 else created + timedelta(hours=random.randint(1, 72))
            
            ticket = SupportTicket(
                id=f"TICK-{i+1:05d}",
                customer_id=f"CUST-{random.randint(1, 1000):05d}",
                category=random.choice(categories),
                priority=random.choice(priorities),
                status="open" if resolved is None else random.choice(["resolved", "closed"]),
                created_at=created,
                resolved_at=resolved,
                satisfaction_rating=random.uniform(6.0, 10.0) if resolved else None,
                churn_risk_flag=random.random() < 0.15
            )
            self.tickets[ticket.id] = ticket
        
        # Employees
        departments = ["sales", "marketing", "finance", "operations", "support", "hr", "it", "legal"]
        roles = {
            "sales": ["Sales Rep", "Account Executive", "Sales Manager", "VP Sales", "Chief Revenue Officer"],
            "marketing": ["Marketing Associate", "Campaign Manager", "Brand Manager", "Director Marketing", "CMO"],
            "finance": ["Financial Analyst", "Accountant", "Finance Manager", "VP Finance", "CFO"],
            "operations": ["Operations Associate", "Process Analyst", "Operations Manager", "VP Operations", "COO"],
            "support": ["Support Agent", "Team Lead", "Support Manager", "VP Support", "VP CX"],
            "hr": ["HR Coordinator", "Recruiter", "HR Manager", "VP HR", "CHRO"],
            "it": ["Developer", "System Admin", "IT Manager", "VP Engineering", "CTO"],
            "legal": ["Paralegal", "Attorney", "Legal Counsel", "Associate General Counsel", "General Counsel"]
        }
        levels = ["entry", "mid", "senior", "lead", "executive"]
        
        for i in range(150):
            dept = random.choice(departments)
            level = random.choice(levels)
            role = roles[dept][levels.index(level)]
            
            base_salary = {
                "entry": 45000, "mid": 70000, "senior": 105000,
                "lead": 145000, "executive": 225000
            }[level]
            
            employee = Employee(
                id=f"EMP-{i+1:04d}",
                name=f"Employee {i+1}",
                department=dept,
                role=role,
                level=level,
                salary=base_salary * random.uniform(0.9, 1.2),
                hire_date=datetime.now() - timedelta(days=random.randint(30, 1825)),
                performance_rating=random.uniform(2.5, 5.0),
                utilization_rate=random.uniform(0.6, 0.95),
                cost_center=dept.upper()
            )
            self.employees[employee.id] = employee
        
        # Financial History (Last 8 quarters)
        for i in range(8):
            quarter = f"Q{(i % 4) + 1} {2023 + (i // 4)}"
            revenue = 125000000 + (i * 2500000) + random.uniform(-2000000, 2000000)
            loss_ratio = 0.68 + random.uniform(-0.03, 0.03)
            cogs = revenue * loss_ratio
            gross_profit = revenue - cogs
            opex = revenue * 0.22 + random.uniform(-1000000, 1000000)
            
            metrics = FinancialMetrics(
                period=quarter,
                revenue=revenue,
                cogs=cogs,
                gross_profit=gross_profit,
                opex=opex,
                ebitda=gross_profit - opex,
                cash_flow=gross_profit - opex + random.uniform(2000000, 5000000),
                loss_ratio=loss_ratio,
                combined_ratio=loss_ratio + (opex / revenue),
                cac=random.uniform(850, 1100),
                ltv=random.uniform(4500, 5500),
                ltv_cac_ratio=random.uniform(4.5, 5.5),
                retention_rate=0.84 + random.uniform(-0.02, 0.02)
            )
            self.financial_history.append(metrics)
    
    # Query Methods
    
    def get_customers_by_segment(self, segment: str) -> List[Customer]:
        """Get customers filtered by segment."""
        return [c for c in self.customers.values() if c.segment == segment]
    
    def get_customers_by_churn_risk(self, threshold: float = 0.7) -> List[Customer]:
        """Get customers with churn risk above threshold."""
        return [c for c in self.customers.values() if c.churn_risk_score >= threshold]
    
    def get_high_value_customers(self, min_premium: float = 5000) -> List[Customer]:
        """Get customers with premium above threshold."""
        return [c for c in self.customers.values() if c.premium >= min_premium]
    
    def get_pipeline_by_stage(self) -> Dict[str, List[SalesOpportunity]]:
        """Group opportunities by stage."""
        result = {}
        for opp in self.opportunities.values():
            if opp.stage not in result:
                result[opp.stage] = []
            result[opp.stage].append(opp)
        return result
    
    def get_pipeline_value(self) -> float:
        """Get total weighted pipeline value."""
        return sum(opp.estimated_value * opp.probability for opp in self.opportunities.values())
    
    def get_campaign_roi(self, campaign_id: str) -> float:
        """Calculate ROI for a specific campaign."""
        camp = self.campaigns.get(campaign_id)
        if not camp or camp.spent == 0:
            return 0.0
        return (camp.revenue_attributed - camp.spent) / camp.spent
    
    def get_support_metrics(self) -> Dict[str, Any]:
        """Get aggregated support metrics."""
        total = len(self.tickets)
        open_tickets = len([t for t in self.tickets.values() if t.status == "open"])
        resolved = [t for t in self.tickets.values() if t.resolved_at]
        
        avg_resolution = None
        if resolved:
            avg_resolution = sum(
                (t.resolved_at - t.created_at).total_seconds() / 3600 
                for t in resolved
            ) / len(resolved)
        
        satisfaction = [t.satisfaction_rating for t in resolved if t.satisfaction_rating]
        avg_satisfaction = sum(satisfaction) / len(satisfaction) if satisfaction else None
        
        return {
            "total_tickets": total,
            "open_tickets": open_tickets,
            "resolution_rate": len(resolved) / total if total > 0 else 0,
            "avg_resolution_hours": avg_resolution,
            "avg_satisfaction": avg_satisfaction,
            "churn_risk_flags": len([t for t in self.tickets.values() if t.churn_risk_flag])
        }
    
    def get_headcount_by_department(self) -> Dict[str, int]:
        """Get employee count by department."""
        result = {}
        for emp in self.employees.values():
            result[emp.department] = result.get(emp.department, 0) + 1
        return result
    
    def get_current_quarter_metrics(self) -> FinancialMetrics:
        """Get the most recent financial metrics."""
        return self.financial_history[-1] if self.financial_history else None
    
    def get_retention_rate(self) -> float:
        """Get current retention rate from financial metrics."""
        metrics = self.get_current_quarter_metrics()
        return metrics.retention_rate if metrics else 0.84
    
    def get_cac(self) -> float:
        """Get current customer acquisition cost."""
        metrics = self.get_current_quarter_metrics()
        return metrics.cac if metrics else 950
    
    def get_policy_performance(self, policy_type: str) -> Optional[Policy]:
        """Get performance data for a specific policy type."""
        for policy in self.policies.values():
            if policy.type == policy_type:
                return policy
        return None


# Singleton instance
_data_store = None

def get_data_store() -> EnterpriseDataStore:
    """Get the singleton data store instance."""
    global _data_store
    if _data_store is None:
        _data_store = EnterpriseDataStore()
    return _data_store


# Example usage and data verification
if __name__ == "__main__":
    store = get_data_store()
    
    print("=== Enterprise Data Store Summary ===\n")
    
    print(f"Customers: {len(store.customers)}")
    print(f"  - High churn risk (>0.7): {len(store.get_customers_by_churn_risk())}")
    print(f"  - High value (>$5k premium): {len(store.get_high_value_customers())}")
    
    print(f"\nSales Pipeline:")
    print(f"  - Total opportunities: {len(store.opportunities)}")
    print(f"  - Weighted pipeline value: ${store.get_pipeline_value():,.0f}")
    
    print(f"\nMarketing Campaigns: {len(store.campaigns)}")
    total_revenue = sum(c.revenue_attributed for c in store.campaigns.values())
    print(f"  - Total attributed revenue: ${total_revenue:,.0f}")
    
    print(f"\nSupport Tickets:")
    metrics = store.get_support_metrics()
    print(f"  - Total: {metrics['total_tickets']}")
    print(f"  - Open: {metrics['open_tickets']}")
    print(f"  - Avg resolution: {metrics['avg_resolution_hours']:.1f} hours")
    print(f"  - Churn risk flags: {metrics['churn_risk_flags']}")
    
    print(f"\nEmployees: {len(store.employees)}")
    print(f"  - By department: {store.get_headcount_by_department()}")
    
    print(f"\nCurrent Quarter Financials:")
    fm = store.get_current_quarter_metrics()
    if fm:
        print(f"  - Revenue: ${fm.revenue:,.0f}")
        print(f"  - Retention rate: {fm.retention_rate:.1%}")
        print(f"  - CAC: ${fm.cac:.0f}")
        print(f"  - LTV:CAC ratio: {fm.ltv_cac_ratio:.1f}x")
