import random
import time

# Function to simulate each node
def process_node(name, principal, years):
    random.seed(principal)  # Unique seed per node
    amount = float(principal)
    days = years * 365
    r = 0.07  # Base interest rate

    # Phase 1 + Phase 2: Daily compounding with delay and randomness
    for _ in range(days):
        b = random.uniform(0.001, 0.009)  # Random bonus
        rate_daily = (r + b) / 365.0
        amount *= (1 + rate_daily)

        # Audit delay
        time.sleep(0.001)

    print(f"{name} Final Amount: {amount:.2f}")
    return amount


if __name__ == "__main__":
    # 🔹 Taking input from user
    P1 = int(input("Enter last 4 digits of Client 1 phone number: "))
    P2 = int(input("Enter last 4 digits of Client 2 phone number: "))
    N = int(input("Enter number of years: "))

    print("\n--- Processing Node A ---")
    amount_A = process_node("Node A", P1, N)

    print("\n--- Processing Node B ---")
    amount_B = process_node("Node B", P2, N)

    # Phase 3: Simulated Message Passing
    print("\n--- Message Passing Phase ---")
    print("Node A sends value to Node B")
    print("Node B sends value to Node A")

    # Phase 4: Consensus
    total_A = amount_A + amount_B
    total_B = amount_B + amount_A

    print(f"\nNode A Computed Total: {total_A:.2f}")
    print(f"Node B Computed Total: {total_B:.2f}")

    # Consensus check
    if abs(total_A - total_B) < 1e-6:
        print("\n✅ Transaction Successful: Consensus Achieved!")
    else:
        print("\n❌ Transaction Failed: Mismatch detected!")