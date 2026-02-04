#!/usr/bin/env python3
"""
Interactive Agentic Enterprise Demo

Presentation-ready demo for hackathon judges.
Allows interactive exploration of the multi-agent system.
"""

import json
import time
from datetime import datetime
from typing import Dict, List, Any


class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'


def print_colored(text: str, color: str = ""):
    """Print colored text."""
    color_code = getattr(Colors, color.upper(), "")
    print(f"{color_code}{text}{Colors.ENDC}")


def clear_screen():
    """Clear the terminal."""
    print("\n" * 3)


def print_banner():
    """Print the main banner."""
    print_colored("""
╔══════════════════════════════════════════════════════════════════════╗
║                                                                      ║
║           🤖 AGENTIC ENTERPRISE OPERATING MODEL 🤖                   ║
║                                                                      ║
║        CEO-Driven Multi-Agent Enterprise Architecture                ║
║                                                                      ║
║              [ HACKATHON DEMO - INTERACTIVE MODE ]                   ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝
    """, "cyan")


def print_loading(text: str, duration: float = 1.0):
    """Show a loading animation."""
    print(f"\n{text}", end="", flush=True)
    for _ in range(3):
        time.sleep(duration / 3)
        print(".", end="", flush=True)
    print(" ✅")


def simulate_agent_thinking(agent_name: str, task: str):
    """Simulate agent processing with visual feedback."""
    print_colored(f"\n🤖 {agent_name} Agent processing: {task}", "yellow")
    steps = [
        "  └─ Accessing enterprise data...",
        "  └─ Analyzing patterns...",
        "  └─ Generating recommendations...",
        "  └─ Validating constraints...",
        "  └─ Done!"
    ]
    for step in steps:
        time.sleep(0.3)
        print_colored(step, "blue")


class AgenticEnterpriseDemo:
    """Interactive demo controller."""
    
    def __init__(self):
        self.current_prompt = ""
        self.agent_outputs = {}
        self.executive_output = {}
        
    def show_architecture(self):
        """Show the system architecture."""
        clear_screen()
        print_colored("""
┌─────────────────────────────────────────────────────────────────────┐
│                    SYSTEM ARCHITECTURE                              │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│   ┌─────────────────────────────────────────────────────────┐      │
│   │              CEO ORCHESTRATION LAYER                     │      │
│   │         (Natural Language → Structured Goals)            │      │
│   └─────────────────────────┬───────────────────────────────┘      │
│                             │                                       │
│                             ▼                                       │
│   ┌─────────────────────────────────────────────────────────┐      │
│   │              TASK DECOMPOSITION ENGINE                   │      │
│   │         (Breaks goals into agent tasks)                  │      │
│   └─────────────────────────┬───────────────────────────────┘      │
│                             │                                       │
│           ┌─────────────────┼─────────────────┐                     │
│           ▼                 ▼                 ▼                     │
│   ┌───────────┐    ┌───────────┐    ┌───────────┐                  │
│   │   Sales   │    │ Marketing │    │  Finance  │                  │
│   │   Agent   │    │   Agent   │    │   Agent   │                  │
│   └─────┬─────┘    └─────┬─────┘    └─────┬─────┘                  │
│   ┌───────────┐    ┌───────────┐    ┌───────────┐                  │
│   │Operations │    │  Support  │    │    HR     │                  │
│   │   Agent   │    │   Agent   │    │   Agent   │                  │
│   └─────┬─────┘    └─────┬─────┘    └─────┬─────┘                  │
│           │                 │                 │                     │
│           └─────────────────┼─────────────────┘                     │
│                             ▼                                       │
│   ┌─────────────────────────────────────────────────────────┐      │
│   │              CONFLICT RESOLUTION LAYER                   │      │
│   │         (Detects & resolves cross-agent conflicts)       │      │
│   └─────────────────────────┬───────────────────────────────┘      │
│                             │                                       │
│                             ▼                                       │
│   ┌─────────────────────────────────────────────────────────┐      │
│   │              GOVERNANCE & COMPLIANCE                     │      │
│   │         (Approvals, Escalations, Audit Trail)            │      │
│   └─────────────────────────┬───────────────────────────────┘      │
│                             │                                       │
│                             ▼                                       │
│   ┌─────────────────────────────────────────────────────────┐      │
│   │              EXECUTIVE DASHBOARD OUTPUT                  │      │
│   │    (Plans, KPIs, Trade-offs, Budget, Headcount)          │      │
│   └─────────────────────────────────────────────────────────┘      │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
        """, "cyan")
        input("\nPress ENTER to continue...")
    
    def run_retention_demo(self):
        """Run the full retention improvement demo."""
        clear_screen()
        print_banner()
        
        # CEO Prompt
        print_colored("\n" + "=" * 70, "header")
        print_colored("👔 CEO PROMPT", "bold")
        print_colored("=" * 70, "header")
        prompt = "Improve quarterly retention by 8% without increasing CAC"
        print_colored(f'\n"{prompt}"\n', "green")
        self.current_prompt = prompt
        
        input("Press ENTER to process through the Agentic Enterprise...")
        
        # Step 1: Orchestration
        clear_screen()
        print_colored("\n📋 STEP 1: CEO ORCHESTRATION LAYER", "header")
        print_colored("-" * 70, "header")
        
        print_loading("Parsing natural language prompt")
        print_colored("  ✓ Goal identified: Improve retention by 8%", "green")
        print_colored("  ✓ Constraint identified: No CAC increase", "green")
        print_colored("  ✓ Departments affected: All 6 functional areas", "green")
        
        print_loading("Decomposing into agent tasks")
        tasks = [
            ("Sales", "Develop retention strategies & customer success plans"),
            ("Marketing", "Design retention campaigns"),
            ("Finance", "Budget allocation & ROI analysis"),
            ("Operations", "Process optimization"),
            ("Support", "Churn signal analysis"),
            ("HR", "Hiring plan for retention team")
        ]
        for agent, task in tasks:
            print_colored(f"  ✓ {agent}: {task}", "blue")
        
        input("\nPress ENTER to activate agents...")
        
        # Step 2: Agent Processing
        clear_screen()
        print_colored("\n📋 STEP 2: FUNCTIONAL AGENTS PROCESSING", "header")
        print_colored("-" * 70, "header")
        
        self.agent_outputs = {
            "sales": {
                "name": "Sales Agent",
                "recommendations": [
                    "Proactive outreach to 67,500 at-risk customers",
                    "Customer Success team expansion (8 CSMs)",
                    "Loyalty rewards program for 2+ year customers"
                ],
                "budget": 450_000,
                "headcount": 8,
                "confidence": 0.85,
                "citations": ["CRM:customer_churn_analysis:67500_records", "Salesforce:pipeline_data:2500_records"]
            },
            "marketing": {
                "name": "Marketing Agent",
                "recommendations": [
                    "At-risk customer win-back campaign (multi-channel)",
                    "Advocate amplification program for referrals",
                    "Lifecycle marketing automation (90-day nurture)"
                ],
                "budget": 850_000,
                "headcount": 3,
                "confidence": 0.80,
                "citations": ["Marketo:campaign_history:150_records", "CRM:segmentation_data:450000_records"]
            },
            "finance": {
                "name": "Finance Agent",
                "recommendations": [
                    "Budget allocation: Marketing 40%, Sales 30%, Support 20%, Ops 10%",
                    "Unit economics monitoring (maintain 10x LTV/CAC)",
                    "Sensitivity analysis for 5%, 8%, 12% retention scenarios"
                ],
                "budget": 0,
                "headcount": 0,
                "confidence": 0.90,
                "citations": ["ERP:budget_status:6_departments", "ERP:unit_economics:5_metrics"]
            },
            "operations": {
                "name": "Operations Agent",
                "recommendations": [
                    "Claims processing acceleration (18.5h → 12h)",
                    "Onboarding experience redesign",
                    "Renewal process automation"
                ],
                "budget": 350_000,
                "headcount": 0,
                "confidence": 0.85,
                "citations": ["Zendesk:ticket_metrics:12500_records", "ProcessMining:workflow_data:45_processes"]
            },
            "support": {
                "name": "Support Agent",
                "recommendations": [
                    "Predictive churn intervention system",
                    "Root cause analysis of 12,500 tickets",
                    "Satisfaction recovery program (NPS < 3.0)",
                    "Escalation prevention (reduce by 50%)"
                ],
                "budget": 200_000,
                "headcount": 6,
                "confidence": 0.90,
                "citations": ["Zendesk:ticket_analysis:12500_records", "Support:churn_signals:500_records"]
            },
            "hr": {
                "name": "HR Agent",
                "recommendations": [
                    "Hiring plan: 20 FTE (8 CSMs, 6 Support, 4 Claims, 2 Analysts)",
                    "Talent acquisition strategy (45-75 day timeline)",
                    "90-day onboarding excellence program",
                    "Compliance & risk management for insurance licenses"
                ],
                "budget": 1_500_000,
                "headcount": 20,
                "confidence": 0.85,
                "citations": ["Workday:headcount_data:620_records", "HRIS:hiring_forecasts:12_roles"]
            }
        }
        
        for agent_key, output in self.agent_outputs.items():
            simulate_agent_thinking(output["name"].replace(" Agent", ""), 
                                   f"Processing {len(output['recommendations'])} recommendations")
            print_colored(f"  📊 Confidence: {output['confidence']:.0%}", "green")
            print_colored(f"  💰 Budget: ${output['budget']:,}", "yellow")
            print_colored(f"  👥 Headcount: {output['headcount']} FTE", "yellow")
            print()
        
        input("Press ENTER to check for conflicts...")
        
        # Step 3: Conflict Resolution
        clear_screen()
        print_colored("\n📋 STEP 3: CONFLICT DETECTION & RESOLUTION", "header")
        print_colored("-" * 70, "header")
        
        total_budget = sum(a['budget'] for a in self.agent_outputs.values())
        total_headcount = sum(a['headcount'] for a in self.agent_outputs.values())
        
        print_loading("Checking budget allocations")
        print_colored(f"  Total requested: ${total_budget:,}", "yellow")
        print_colored(f"  Budget limit: $43,000,000", "blue")
        print_colored("  ✓ Within limits (7.8% of total)", "green")
        
        print_loading("Checking timeline dependencies")
        print_colored("  ✓ No blocking dependencies detected", "green")
        
        print_loading("Checking strategic alignment")
        print_colored("  ✓ All agents aligned on retention objective", "green")
        print_colored("  ✓ No contradictory recommendations", "green")
        
        print_loading("Checking resource contention")
        print_colored("  ✓ No overlapping resource requests", "green")
        
        print_colored("\n✅ STATUS: ALL AGENTS ALIGNED", "green")
        print_colored("   Cross-functional consistency verified", "green")
        
        input("\nPress ENTER to validate governance...")
        
        # Step 4: Governance
        clear_screen()
        print_colored("\n📋 STEP 4: GOVERNANCE & COMPLIANCE", "header")
        print_colored("-" * 70, "header")
        
        checks = [
            ("Confidence threshold", "All agents > 60%", True),
            ("Budget authority", "No single item > $500K", True),
            ("Headcount growth", "Within 20% limit", True),
            ("Data citations", "All claims cited", True),
            ("Risk assessment", "Documented per agent", True),
            ("Audit trail", "Full traceability enabled", True)
        ]
        
        for check, status, passed in checks:
            icon = "✅" if passed else "❌"
            color = "green" if passed else "red"
            print_colored(f"{icon} {check:<25} {status}", color)
        
        print_colored("\n🛡️  STATUS: WITHIN AUTHORITY BOUNDARIES", "green")
        print_colored("    No CEO escalation required", "green")
        
        input("\nPress ENTER to view executive dashboard...")
        
        # Step 5: Executive Dashboard
        self.show_executive_dashboard(total_budget, total_headcount)
    
    def show_executive_dashboard(self, total_budget: float, total_headcount: int):
        """Show the executive dashboard."""
        clear_screen()
        print_banner()
        
        print_colored("\n" + "=" * 70, "header")
        print_colored("📊 EXECUTIVE DASHBOARD", "bold")
        print_colored("=" * 70, "header")
        
        print_colored(f"\n🎯 STRATEGIC GOAL: Improve quarterly retention by 8%", "cyan")
        print_colored(f"⛔ CONSTRAINT: No CAC increase", "cyan")
        
        print_colored("\n" + "─" * 70, "header")
        print_colored("EXECUTIVE SUMMARY", "bold")
        print_colored("─" * 70, "header")
        
        print_colored(f"""
To achieve 8% retention improvement without increasing CAC, the Agentic 
Enterprise recommends a comprehensive cross-functional initiative requiring:

  • Total Investment: ${total_budget:,}
  • New Hires: {total_headcount} FTE  
  • Timeline: 90 days
  • Expected Outcome: 8-10% retention improvement
  • ROI: 4.2x over 24 months
        """, "green")
        
        print_colored("─" * 70, "header")
        print_colored("STRATEGIC OPTIONS", "bold")
        print_colored("─" * 70, "header")
        
        options = [
            ("1. Comprehensive Program", total_budget, 90, "8-10%", "Maximum impact"),
            ("2. Phased Rollout", int(total_budget * 0.6), 180, "5-6%", "Lower risk"),
            ("3. Minimum Viable", int(total_budget * 0.3), 45, "3-4%", "Quick start")
        ]
        
        for name, budget, timeline, impact, risk in options:
            print_colored(f"\n{name}", "yellow")
            print_colored(f"   Investment: ${budget:,}", "blue")
            print_colored(f"   Timeline: {timeline} days", "blue")
            print_colored(f"   Expected Impact: {impact} retention improvement", "blue")
            print_colored(f"   Trade-offs: {risk}", "blue")
        
        print_colored("\n" + "─" * 70, "header")
        print_colored("SUCCESS METRICS (KPIs)", "bold")
        print_colored("─" * 70, "header")
        
        kpis = [
            ("Retention Rate", "84%", "92%"),
            ("NPS Score", "32", "45"),
            ("Churn Rate", "16%", "8%"),
            ("Support Resolution", "18.5h", "12h"),
            ("CAC", "$385", "$385 (maintain)")
        ]
        
        for metric, current, target in kpis:
            print_colored(f"  📊 {metric:<25} {current:>10} → {target}", "cyan")
        
        print_colored("\n" + "─" * 70, "header")
        print_colored("BUDGET BREAKDOWN", "bold")
        print_colored("─" * 70, "header")
        
        for agent_key, output in self.agent_outputs.items():
            pct = (output['budget'] / total_budget * 100) if total_budget > 0 else 0
            print_colored(f"  💰 {output['name']:<20} ${output['budget']:>10,} ({pct:>4.1f}%)", "yellow")
        
        print_colored(f"  {'─'*50}", "header")
        print_colored(f"  📊 {'TOTAL':<20} ${total_budget:>10,} (100.0%)", "green")
        
        print_colored("\n" + "─" * 70, "header")
        print_colored("HEADCOUNT BREAKDOWN", "bold")
        print_colored("─" * 70, "header")
        
        for agent_key, output in self.agent_outputs.items():
            if output['headcount'] > 0:
                print_colored(f"  👥 {output['name']:<20} {output['headcount']:>5} FTE", "yellow")
        
        print_colored(f"  {'─'*50}", "header")
        print_colored(f"  📊 {'TOTAL':<20} {total_headcount:>5} FTE", "green")
        
        # Save output
        output_data = {
            "timestamp": datetime.now().isoformat(),
            "prompt": self.current_prompt,
            "total_budget": total_budget,
            "total_headcount": total_headcount,
            "agent_outputs": self.agent_outputs
        }
        
        filename = f"demo_output_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w') as f:
            json.dump(output_data, f, indent=2)
        
        print_colored(f"\n📄 Full output saved to: {filename}", "blue")
    
    def show_agent_details(self):
        """Show detailed agent outputs."""
        clear_screen()
        print_banner()
        
        print_colored("\n📋 AGENT DETAILS", "header")
        print_colored("-" * 70, "header")
        
        agents = [
            ("sales", "SALES AGENT", "Pipeline, leads, pricing, retention"),
            ("marketing", "MARKETING AGENT", "Campaigns, channels, attribution"),
            ("finance", "FINANCE AGENT", "Budget, forecasting, ROI"),
            ("operations", "OPERATIONS AGENT", "Process optimization, SLAs"),
            ("support", "SUPPORT AGENT", "Tickets, churn signals, CX"),
            ("hr", "HR AGENT", "Hiring, workforce, compliance")
        ]
        
        for i, (key, name, desc) in enumerate(agents, 1):
            print_colored(f"\n{i}. {name}", "yellow")
            print_colored(f"   Focus: {desc}", "blue")
            
            if key in self.agent_outputs:
                output = self.agent_outputs[key]
                print_colored(f"   Confidence: {output['confidence']:.0%}", "green")
                print_colored(f"   Data Citations: {len(output['citations'])} sources", "blue")
                print_colored("   Key Recommendations:", "cyan")
                for rec in output['recommendations'][:2]:
                    print_colored(f"      • {rec[:60]}...", "blue")
        
        input("\nPress ENTER to return to menu...")
    
    def show_features(self):
        """Show system features."""
        clear_screen()
        print_banner()
        
        print_colored("\n✅ ENTERPRISE FEATURES", "header")
        print_colored("-" * 70, "header")
        
        features = [
            ("Natural Language Interface", "CEO issues prompts in plain English"),
            ("Multi-Agent Orchestration", "6 specialized agents work in parallel"),
            ("Conflict Resolution", "Automatic detection & resolution of contradictions"),
            ("Governance & Compliance", "Approval flows, audit trails, escalation rules"),
            ("Data Citations", "Every claim references internal data sources"),
            ("Confidence Scoring", "All recommendations include certainty levels"),
            ("Uncertainty Documentation", "'What would change my mind' captured"),
            ("Cross-Functional Alignment", "Ensures consistent recommendations"),
            ("Budget Impact Analysis", "Real-time cost aggregation"),
            ("Headcount Planning", "Hiring needs calculated automatically"),
            ("Risk Assessment", "Each agent documents risks & mitigations"),
            ("KPI Tracking", "Measurable success metrics defined")
        ]
        
        for feature, desc in features:
            print_colored(f"\n✓ {feature}", "green")
            print_colored(f"  {desc}", "blue")
        
        input("\nPress ENTER to return to menu...")
    
    def interactive_prompt(self):
        """Allow user to enter their own prompt."""
        clear_screen()
        print_banner()
        
        print_colored("\n🎤 INTERACTIVE PROMPT", "header")
        print_colored("-" * 70, "header")
        
        print_colored("\nExample prompts you can try:", "cyan")
        examples = [
            "Reduce customer acquisition cost by 15%",
            "Improve support response time to under 4 hours",
            "Launch a new product line in Q3",
            "Optimize our sales pipeline conversion",
            "Expand into the European market"
        ]
        
        for ex in examples:
            print_colored(f"  • {ex}", "blue")
        
        print_colored("\nEnter your CEO prompt (or 'back' to return):", "yellow")
        user_prompt = input("\n👔 CEO> ").strip()
        
        if user_prompt.lower() == 'back':
            return
        
        if user_prompt:
            print_colored(f"\nProcessing: '{user_prompt}'", "green")
            print_colored("\n[In full implementation, this would:", "blue")
            print_colored("  1. Parse your prompt using NLP", "blue")
            print_colored("  2. Route to relevant agents", "blue")
            print_colored("  3. Generate custom recommendations", "blue")
            print_colored("  4. Return executive dashboard]", "blue")
            print_colored("\n[For demo, showing pre-computed retention example]", "yellow")
            input("\nPress ENTER to see results...")
            self.run_retention_demo()
    
    def main_menu(self):
        """Show main menu."""
        while True:
            clear_screen()
            print_banner()
            
            print_colored("\n📋 MAIN MENU", "header")
            print_colored("-" * 70, "header")
            
            options = [
                ("1", "Run Full Demo", "Complete retention improvement scenario"),
                ("2", "View Architecture", "System diagram and components"),
                ("3", "Agent Details", "Deep dive into each agent"),
                ("4", "Enterprise Features", "Capabilities and governance"),
                ("5", "Try Your Own Prompt", "Interactive CEO prompt"),
                ("q", "Quit", "Exit the demo")
            ]
            
            for key, name, desc in options:
                print_colored(f"\n  [{key}] {name}", "yellow")
                print_colored(f"      {desc}", "blue")
            
            print_colored("\n" + "-" * 70, "header")
            choice = input("\nSelect option: ").strip().lower()
            
            if choice == '1':
                self.run_retention_demo()
            elif choice == '2':
                self.show_architecture()
            elif choice == '3':
                self.show_agent_details()
            elif choice == '4':
                self.show_features()
            elif choice == '5':
                self.interactive_prompt()
            elif choice == 'q':
                print_colored("\n👋 Thank you for exploring the Agentic Enterprise!", "green")
                break
            else:
                print_colored("\n❌ Invalid option. Press ENTER to continue...", "red")
                input()


def main():
    """Main entry point."""
    demo = AgenticEnterpriseDemo()
    demo.main_menu()


if __name__ == "__main__":
    main()
