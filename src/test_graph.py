"""
Autonomous Graph Integration Test Script
Author: Dhiraj Malwade
"""
import sys
import os
from dotenv import load_dotenv

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.graph_engine import invoke_graph_autonomous

def test_autonomous_state_machine():
    load_dotenv()
    ticker = "NVDA"
    
    final_state = invoke_graph_autonomous(ticker)
    
    print("\n--- AUTONOMOUS EXECUTION RESULTS ---")
    print(f"Company Target: {final_state.get('company_name')}")
    print(f"Current Price:  {final_state.get('current_price')}")
    print(f"Change (24h):   {final_state.get('change_percent')}")
    print(f"Verified:       {final_state.get('verified')}")
    print("\n--- FORMATTED BRIEF ---")
    print(final_state.get('final_brief', 'No brief generated.'))
    
    if final_state.get('final_brief') and final_state.get('verified'):
        print("\n[SUCCESS] Phase 4 Autonomous Graph executed successfully.")
    else:
        print("\n[ERROR] Graph execution failed or intelligence was unverified.")

if __name__ == "__main__":
    test_autonomous_state_machine()