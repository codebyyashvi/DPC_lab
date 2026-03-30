import json
import time

with open("seed.json") as f:
    data = json.load(f)

N = 5
theta = data["theta"]
clocks = data["clocks"]
queues = data["queues"]

print("\n--- CLOCK SYNCHRONIZATION START ---\n")
time.sleep(1)

T0 = clocks[0]

S = [i for i in range(N) if abs(clocks[i] - T0) <= theta]

print(f"Trusted Nodes: {S}")
time.sleep(1)

T_target = sum(clocks[i] for i in S) // len(S)

print(f"Target Time: {T_target}\n")
time.sleep(1)

delta = [0] * N
T_sync = [0] * N

for i in range(N):
    if i in S:
        delta[i] = T_target - clocks[i]
    else:
        delta[i] = 0
    T_sync[i] = clocks[i] + delta[i]
    print(f"Node {i}: Initial={clocks[i]}, Delta={delta[i]}, Synced={T_sync[i]}")
    time.sleep(0.5)

print("\n--- CLOCK SYNCHRONIZATION END ---\n")
time.sleep(1)

print("--- MESSAGE PROCESSING START ---\n")

V = [[0]*N for _ in range(N)]

buffers = [[] for _ in range(N)]

def can_process(i, sender, v_msg):
    if v_msg[sender] != V[i][sender] + 1:
        return False
    for k in range(N):
        if k != sender and v_msg[k] > V[i][k]:
            return False
    return True

def process_message(i, msg):
    sender = msg["sender"]
    v_msg = msg["v_msg"]
    print(f"Node {i} RECEIVED msg from {sender} -> {v_msg}")
    time.sleep(0.4)
    if can_process(i, sender, v_msg):
        print(f"Node {i} PROCESSED message from {sender}")
        for k in range(N):
            V[i][k] = max(V[i][k], v_msg[k])
        time.sleep(0.4)
        return True
    else:
        print(f"Node {i} BUFFERED message from {sender}")
        buffers[i].append(msg)
        time.sleep(0.4)
        return False

def try_buffer(i):
    changed = True
    while changed:
        changed = False
        for msg in buffers[i][:]:
            if can_process(i, msg["sender"], msg["v_msg"]):
                print(f"Node {i} RELEASED buffered msg from {msg['sender']}")
                for k in range(N):
                    V[i][k] = max(V[i][k], msg["v_msg"][k])
                buffers[i].remove(msg)
                time.sleep(0.4)
                changed = True

for i in range(N):
    print(f"\nProcessing Node {i} Queue\n")
    time.sleep(0.8)

    for msg in queues[i]:
        process_message(i, msg)
        try_buffer(i)

    try_buffer(i)

print("\n--- MESSAGE PROCESSING END ---")
time.sleep(1)

print("\n--- FINAL PAYLOADS ---\n")

P = [0]*N

for i in range(N):
    total_v = sum(V[i])
    P[i] = (T_sync[i] * total_v) % 9973
    print(f"Node {i}: V = {V[i]}, Sum = {total_v}, Payload = {P[i]}")
    time.sleep(0.5)

print("\n--- DONE ---\n")