import multiprocessing as mp
import time
import random
from datetime import datetime

def node_process(
    node_name,
    principal,
    phone_seed,
    years,
    message_queue_send,
    message_queue_recv
):
    
    random.seed(phone_seed)
    base_rate = 0.07 
    amount = float(principal)
    
    total_days = years * 365
    
    print(f"\n[NODE {node_name}] Starting Compound Interest Calculation")
    print(f"[NODE {node_name}] Principal: ${amount:.2f}")
    print(f"[NODE {node_name}] Time Period: {years} year(s) ({total_days} days)")
    print(f"[NODE {node_name}] Random Seed (Phone): {phone_seed}")
    print(f"[NODE {node_name}] Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"[NODE {node_name}] " + "="*60)
    
    # Phase 1: Daily Calculation with Delays
    for day in range(1, total_days + 1):
        # Phase 2: Generate randomized market bonus (0.1% to 0.9%)
        market_bonus = random.uniform(0.001, 0.009)
        
        # Calculate daily rate
        daily_rate = (base_rate + market_bonus) / 365.0
        
        # Apply compound interest
        amount = amount * (1 + daily_rate)
        
        # Audit Delay (regulatory requirement)
        # Small delay to simulate cryptographic audit
        time.sleep(0.001)  # 1ms per day (reasonable for simulation)
        
        # Progress indicator every 365 days (yearly)
        if day % 365 == 0:
            year_count = day // 365
            print(f"[NODE {node_name}] Year {year_count}: ${amount:.2f}")
    
    # Phase 1 Complete: Calculate final maturity value
    maturity_value = amount
    
    print(f"\n[NODE {node_name}] Calculation Complete!")
    print(f"[NODE {node_name}] Final Maturity Value: ${maturity_value:.2f}")
    print(f"[NODE {node_name}] Total Interest Earned: ${maturity_value - principal:.2f}")
    
    # Phase 3: Communication Protocol
    print(f"\n[NODE {node_name}] Entering Communication Phase...")
    
    # Send maturity value to other node
    message_queue_send.put(maturity_value)
    print(f"[NODE {node_name}] Sent Maturity Value: ${maturity_value:.2f}")
    
    # Receive maturity value from other node
    other_maturity = message_queue_recv.get()
    print(f"[NODE {node_name}] Received Maturity Value: ${other_maturity:.2f}")
    
    # Phase 4: Consensus Check
    print(f"\n[NODE {node_name}] Entering Consensus Phase...")
    
    total = maturity_value + other_maturity
    
    print(f"[NODE {node_name}] My Maturity: ${maturity_value:.2f}")
    print(f"[NODE {node_name}] Other Maturity: ${other_maturity:.2f}")
    print(f"[NODE {node_name}] Final Total: ${total:.2f}")
    
    # Both nodes should calculate the same total
    if abs(maturity_value - other_maturity) < 0.01:
        print(f"\n[NODE {node_name}] ✓ CONSENSUS VERIFIED: Transaction Successful!")
    else:
        print(f"\n[NODE {node_name}] ✗ CONSENSUS FAILED: Values do not match!")
    
    print(f"[NODE {node_name}] Ended at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    return {
        'node': node_name,
        'principal': principal,
        'maturity': maturity_value,
        'total': total
    }


def main():
    """
    Main function to orchestrate the joint deposit processing.
    """
    
    print("\n" + "="*70)
    print("  DISTRIBUTED BANKING SYSTEM - JOINT FIXED DEPOSIT ACCOUNT")
    print("  CS-302 | Distributed & Parallel Computing Lab")
    print("="*70)
    
    # Configuration
    print("\n[SETUP] Configuring Joint Account Parameters...")
    
    # For demonstration, using example phone numbers
    # In production, these would be provided by users
    phone1 = input("[INPUT] Enter last 4 digits of Client 1's phone number (or press Enter for 1234): ").strip()
    phone1 = int(phone1) if phone1.isdigit() and len(phone1) == 4 else 1234
    
    phone2 = input("[INPUT] Enter last 4 digits of Client 2's phone number (or press Enter for 5678): ").strip()
    phone2 = int(phone2) if phone2.isdigit() and len(phone2) == 4 else 5678
    
    years = input("[INPUT] Enter timeframe in years (or press Enter for 5): ").strip()
    years = int(years) if years.isdigit() and int(years) > 0 else 5
    
    # Principal amounts derived from phone numbers
    p1 = float(phone1)
    p2 = float(phone2)
    
    print(f"\n[SETUP] Joint Account Configuration:")
    print(f"  Client 1 Principal (P1): ${p1:.2f}")
    print(f"  Client 2 Principal (P2): ${p2:.2f}")
    print(f"  Total Joint Deposit: ${p1 + p2:.2f}")
    print(f"  Time Period: {years} year(s)")
    print(f"  Compound Interest: Daily (365 days/year)")
    
    # Create message passing queues for IPC
    # Node A sends to queue_a_to_b, receives from queue_b_to_a
    queue_a_to_b = mp.Queue()
    queue_b_to_a = mp.Queue()
    
    print(f"\n[SETUP] Creating independent computational nodes...")
    print(f"[SETUP] Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Create and start Node A and Node B processes
    start_time = time.time()
    
    node_a = mp.Process(
        target=node_process,
        args=('A', p1, phone1, years, queue_a_to_b, queue_b_to_a)
    )
    
    node_b = mp.Process(
        target=node_process,
        args=('B', p2, phone2, years, queue_b_to_a, queue_a_to_b)
    )
    
    # Start both nodes
    node_a.start()
    node_b.start()
    
    # Wait for both nodes to complete
    node_a.join()
    node_b.join()
    
    elapsed_time = time.time() - start_time
    
    # Summary
    print(f"\n" + "="*70)
    print("  TRANSACTION SUMMARY")
    print("="*70)
    print(f"Total Computation Time: {elapsed_time:.2f} seconds")
    print(f"\n[SUMMARY] Joint Fixed Deposit Processing Complete")
    print(f"[SUMMARY] Both nodes processed independently with:")
    print(f"  • Daily compound interest calculation")
    print(f"  • Randomized market fluctuations (seed-based)")
    print(f"  • Regulatory audit delays")
    print(f"  • Distributed message passing protocol")
    print(f"  • Consensus verification")
    print(f"\n[SUMMARY] Ended at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*70 + "\n")


if __name__ == '__main__':
    main()
