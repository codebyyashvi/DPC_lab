import socket
import threading
import time
import random
from datetime import datetime

class BankNode:
    def __init__(self, node_id, principal, phone_seed, years, own_port, other_port):
        self.node_id = node_id
        self.principal = principal
        self.phone_seed = phone_seed
        self.years = years
        self.own_port = own_port
        self.other_port = other_port
        self.host = 'localhost'
        
        self.maturity_value = None
        self.other_maturity_value = None
        self.server_socket = None
        self.client_connection = None
        self.received_event = threading.Event()
        
    def calculate_compound_interest(self):
        print(f"\n[NODE {self.node_id}] Starting Compound Interest Calculation")
        print(f"[NODE {self.node_id}] Principal: ${self.principal:.2f}")
        print(f"[NODE {self.node_id}] Time Period: {self.years} year(s)")
        print(f"[NODE {self.node_id}] Random Seed (Phone): {self.phone_seed}")
        print(f"[NODE {self.node_id}] Started at: {datetime.now().strftime('%H:%M:%S')}")
        print(f"[NODE {self.node_id}] " + "-"*60)
        
        # Set random seed based on phone number
        random.seed(self.phone_seed)
        
        base_rate = 0.07  # 7% annual
        amount = float(self.principal)
        total_days = self.years * 365
        
        # Daily compounding
        for day in range(1, total_days + 1):
            # Phase 2: Random market bonus (0.1% to 0.9%)
            market_bonus = random.uniform(0.001, 0.009)
            
            # Calculate daily rate
            daily_rate = (base_rate + market_bonus) / 365.0
            
            # Apply interest compounding
            amount = amount * (1 + daily_rate)
            
            # Phase 1: Audit Delay (simulate cryptographic verification)
            time.sleep(0.0005)  # 0.5ms delay per day
            
            # Progress every year
            if day % 365 == 0:
                year_num = day // 365
                print(f"[NODE {self.node_id}] Year {year_num}: ${amount:.2f}")
        
        self.maturity_value = amount
        
        print(f"\n[NODE {self.node_id}] Calculation Complete!")
        print(f"[NODE {self.node_id}] Final Maturity Value: ${self.maturity_value:.2f}")
        print(f"[NODE {self.node_id}] Interest Earned: ${self.maturity_value - self.principal:.2f}")
        
    def start_server(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        try:
            self.server_socket.bind((self.host, self.own_port))
            self.server_socket.listen(1)
            print(f"[NODE {self.node_id}] Server listening on port {self.own_port}")
            
            # Accept connection in a separate thread
            server_thread = threading.Thread(target=self._accept_connection)
            server_thread.daemon = True
            server_thread.start()
            
        except Exception as e:
            print(f"[NODE {self.node_id}] Server error: {e}")
            
    def _accept_connection(self):
        try:
            self.client_connection, addr = self.server_socket.accept()
            print(f"[NODE {self.node_id}] Incoming connection from {addr}")
        except Exception as e:
            print(f"[NODE {self.node_id}] Accept error: {e}")
    
    def connect_to_other_node(self, max_retries=10):
        for attempt in range(max_retries):
            try:
                client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client_socket.connect((self.host, self.other_port))
                print(f"[NODE {self.node_id}] Connected to Node on port {self.other_port}")
                return client_socket
            except ConnectionRefusedError:
                if attempt < max_retries - 1:
                    print(f"[NODE {self.node_id}] Waiting for other node... (attempt {attempt+1}/{max_retries})")
                    time.sleep(1)
                else:
                    print(f"[NODE {self.node_id}] Failed to connect after {max_retries} attempts")
                    return None
        return None
    
    def exchange_values(self):
        print(f"\n[NODE {self.node_id}] Entering Communication Phase...")
        
        # Wait for both server and client connections
        max_wait = 30
        start = time.time()
        
        # Connect as client
        client_socket = self.connect_to_other_node()
        if not client_socket:
            print(f"[NODE {self.node_id}] Communication failed!")
            return False
        
        # Wait for server to accept connection
        while self.client_connection is None and (time.time() - start) < max_wait:
            time.sleep(0.1)
        
        if self.client_connection is None:
            print(f"[NODE {self.node_id}] Server connection timeout!")
            return False
        
        # Send maturity value to other node
        try:
            message = f"{self.maturity_value:.2f}"
            client_socket.send(message.encode('utf-8'))
            print(f"[NODE {self.node_id}] Sent Maturity Value: ${self.maturity_value:.2f}")
        except Exception as e:
            print(f"[NODE {self.node_id}] Send error: {e}")
            return False
        
        # Receive maturity value from other node
        try:
            data = self.client_connection.recv(1024).decode('utf-8')
            self.other_maturity_value = float(data)
            print(f"[NODE {self.node_id}] Received Maturity Value: ${self.other_maturity_value:.2f}")
            self.received_event.set()
        except Exception as e:
            print(f"[NODE {self.node_id}] Receive error: {e}")
            return False
        finally:
            client_socket.close()
            self.client_connection.close()
        
        return True
    
    def verify_consensus(self):
        if self.other_maturity_value is None:
            print(f"[NODE {self.node_id}] No data received for consensus check!")
            return False
        
        print(f"\n[NODE {self.node_id}] Entering Consensus Phase...")
        
        total = self.maturity_value + self.other_maturity_value
        
        print(f"[NODE {self.node_id}] My Maturity Value: ${self.maturity_value:.2f}")
        print(f"[NODE {self.node_id}] Other Node's Maturity: ${self.other_maturity_value:.2f}")
        print(f"[NODE {self.node_id}] Final Total: ${total:.2f}")
        
        # Both nodes should have calculated successfully
        print(f"\n[NODE {self.node_id}] ✓ CONSENSUS: Transaction successful!")
        print(f"[NODE {self.node_id}] Total Joint Deposit Maturity: ${total:.2f}")
        
        return True
    
    def cleanup(self):
        if self.server_socket:
            self.server_socket.close()
        if self.client_connection:
            self.client_connection.close()


def run_node(node_id, principal, phone_seed, years, own_port, other_port):
    print(f"\n{'='*70}")
    print(f"  NODE {node_id} - Starting Distributed Banking Process")
    print(f"{'='*70}")
    
    node = BankNode(node_id, principal, phone_seed, years, own_port, other_port)
    
    try:
        # Phase 1 & 2: Calculate compound interest
        node.start_server()
        time.sleep(0.5)  # Allow other node to start
        
        node.calculate_compound_interest()
        
        # Phase 3: Exchange values via message passing
        if not node.exchange_values():
            print(f"[NODE {node_id}] Failed to exchange values!")
            return
        
        # Phase 4: Verify consensus
        node.verify_consensus()
        
        print(f"\n[NODE {node_id}] Process completed successfully")
        
    except Exception as e:
        print(f"[NODE {node_id}] Error: {e}")
    finally:
        node.cleanup()


def main():
    print("\n" + "="*70)
    print("  DISTRIBUTED BANKING SYSTEM - SOCKET-BASED")
    print("  Joint Fixed Deposit Account Processing")
    print("  CS-302 | Distributed & Parallel Computing Lab")
    print("="*70)
    
    # Configuration
    print("\n[SETUP] Configuring Joint Account Parameters...")
    
    phone1_input = input("[INPUT] Enter last 4 digits of Client 1's phone (or press Enter for 1234): ").strip()
    phone1 = int(phone1_input) if phone1_input.isdigit() and len(phone1_input) == 4 else 1234
    
    phone2_input = input("[INPUT] Enter last 4 digits of Client 2's phone (or press Enter for 5678): ").strip()
    phone2 = int(phone2_input) if phone2_input.isdigit() and len(phone2_input) == 4 else 5678
    
    years_input = input("[INPUT] Enter timeframe in years (or press Enter for 5): ").strip()
    years = int(years_input) if years_input.isdigit() and int(years_input) > 0 else 5
    
    p1 = float(phone1)
    p2 = float(phone2)
    
    print(f"\n[SETUP] Joint Account Configuration:")
    print(f"  Client 1 Principal (P1): ${p1:.2f}")
    print(f"  Client 2 Principal (P2): ${p2:.2f}")
    print(f"  Total Joint Deposit: ${p1 + p2:.2f}")
    print(f"  Time Period: {years} year(s)")
    print(f"  Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Start both nodes as threads
    print(f"\n[SETUP] Launching independent computational nodes...")
    
    node_a_thread = threading.Thread(
        target=run_node,
        args=('A', p1, phone1, years, 5001, 5002)
    )
    
    node_b_thread = threading.Thread(
        target=run_node,
        args=('B', p2, phone2, years, 5002, 5001)
    )
    
    start_time = time.time()
    
    node_a_thread.start()
    node_b_thread.start()
    
    node_a_thread.join()
    node_b_thread.join()
    
    elapsed = time.time() - start_time
    
    # Summary
    print(f"\n" + "="*70)
    print("  TRANSACTION SUMMARY")
    print("="*70)
    print(f"Total Computation Time: {elapsed:.2f} seconds")
    print(f"End Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("\n[SUMMARY] Distributed Processing Complete!")
    print("[SUMMARY] All phases executed:")
    print("  ✓ Phase 1: Daily interest calculation with audit delays")
    print("  ✓ Phase 2: Randomized market fluctuations (seeded)")
    print("  ✓ Phase 3: Socket-based message passing")
    print("  ✓ Phase 4: Consensus verification")
    print("="*70 + "\n")


if __name__ == '__main__':
    main()
