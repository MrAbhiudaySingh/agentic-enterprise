#!/usr/bin/env python3
"""
Agentic Enterprise - CLI Application

Interactive command-line interface for the CEO Orchestration Layer.
"""

import sys
from ceo_orchestrator import get_orchestrator


def print_banner():
    """Print welcome banner."""
    print("""
╔══════════════════════════════════════════════════════════════════════╗
║                                                                      ║
║           🤖 AGENTIC ENTERPRISE OPERATING SYSTEM 🤖                  ║
║                                                                      ║
║        CEO-Driven Multi-Agent Enterprise Architecture                 ║
║              Insurance Company Demonstration                          ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝
    """)


def print_help():
    """Print help information."""
    print("""
Available Commands:
  <prompt>     Enter a strategic prompt for the CEO Orchestrator
  demo         Run the pre-loaded demo scenario
  status       Show current enterprise status
  agents       List available functional agents
  clear        Clear the screen
  help         Show this help message
  quit         Exit the application

Example Prompts:
  • "Improve quarterly retention by 8% without increasing CAC"
  • "Optimize our sales pipeline for Q2"
  • "Reduce customer support resolution time by 30%"
    """)


def print_agents():
    """Print information about functional agents."""
    print("""
┌─────────────────────────────────────────────────────────────────────┐
│                    FUNCTIONAL AGENTS                                │
├─────────────────────────────────────────────────────────────────────┤
│  🎯 Sales Agent          Pipeline, pricing, sales enablement        │
│  📢 Marketing Agent      Campaigns, channels, attribution           │
│  💰 Finance Agent        Budget, forecasting, ROI analysis          │
│  ⚙️  Operations Agent     Process optimization, SLA management       │
│  🎧 Support Agent        Tickets, churn signals, CX insights        │
│  👥 HR Agent             Hiring, workforce, compliance              │
└─────────────────────────────────────────────────────────────────────┘
    """)


def run_demo():
    """Run the pre-loaded demo scenario."""
    print("\n" + "=" * 80)
    print("RUNNING DEMO SCENARIO")
    print("=" * 80)
    print("\nCEO Prompt: 'Improve quarterly retention by 8% without increasing CAC'")
    print("\nInitializing Agentic Enterprise...")
    
    orchestrator = get_orchestrator()
    
    print("✅ Orchestrator initialized")
    print("✅ Shared memory loaded with insurance company data")
    print("✅ 6 functional agents ready")
    print("\nProcessing CEO prompt through multi-agent system...\n")
    
    output = orchestrator.process_prompt(
        "Improve quarterly retention by 8% without increasing CAC"
    )
    
    formatted = orchestrator.format_output_for_display(output)
    print(formatted)
    
    # Save output to file
    filename = f"executive_output_{output.prompt_id}.txt"
    with open(filename, 'w') as f:
        f.write(formatted)
    print(f"\n📄 Output saved to: {filename}")


def show_status():
    """Show current enterprise status."""
    from infrastructure import get_shared_memory, get_enterprise_data
    
    memory = get_shared_memory()
    data = get_enterprise_data()
    
    context = memory.get_company_context()
    summary = data.get_executive_summary()
    
    print("\n" + "=" * 80)
    print("ENTERPRISE STATUS DASHBOARD")
    print("=" * 80)
    
    print(f"\n📅 Current Quarter: {context.quarter}")
    
    print("\n🎯 Company Goals:")
    for goal, value in context.goals.items():
        if isinstance(value, float):
            print(f"   • {goal}: {value:.0%}")
        else:
            print(f"   • {goal}: {value}")
    
    print("\n💼 Customers:")
    cust = summary["customers"]
    print(f"   • Total Customers: {cust['total_customers']:,}")
    print(f"   • High Risk: {cust['high_risk_customers']:,}")
    print(f"   • At-Risk Revenue: ${cust['at_risk_revenue']:,.0f}")
    
    print("\n💵 Financials:")
    unit = summary["unit_economics"]
    print(f"   • CAC: ${unit['cac']:.0f}")
    print(f"   • LTV: ${unit['ltv']:.0f}")
    print(f"   • LTV/CAC Ratio: {unit['ltv_cac_ratio']:.1f}x")
    
    print("\n👥 Headcount:")
    hc = summary["headcount"]
    print(f"   • Current: {hc['total_current']}")
    print(f"   • Target: {hc['total_target']}")
    print(f"   • Open Positions: {hc['total_open_positions']}")


def main():
    """Main CLI loop."""
    print_banner()
    print_help()
    
    orchestrator = None
    
    while True:
        try:
            print("\n" + "─" * 40)
            user_input = input("\n👔 CEO> ").strip()
            
            if not user_input:
                continue
            
            command = user_input.lower()
            
            if command == "quit" or command == "exit":
                print("\nShutting down Agentic Enterprise. Goodbye! 👋")
                break
            
            elif command == "help":
                print_help()
            
            elif command == "agents":
                print_agents()
            
            elif command == "demo":
                run_demo()
            
            elif command == "status":
                show_status()
            
            elif command == "clear":
                print("\n" * 50)
                print_banner()
            
            else:
                # Treat as CEO prompt
                print(f"\n📝 Processing prompt: '{user_input}'")
                print("⏳ Delegating to functional agents...\n")
                
                if orchestrator is None:
                    orchestrator = get_orchestrator()
                
                output = orchestrator.process_prompt(user_input)
                formatted = orchestrator.format_output_for_display(output)
                print(formatted)
                
                # Save output
                filename = f"executive_output_{output.prompt_id}.txt"
                with open(filename, 'w') as f:
                    f.write(formatted)
                print(f"\n📄 Output saved to: {filename}")
        
        except KeyboardInterrupt:
            print("\n\nInterrupted. Type 'quit' to exit.")
        
        except Exception as e:
            print(f"\n❌ Error: {e}")
            import traceback
            traceback.print_exc()


if __name__ == "__main__":
    main()
