import xmlrpc.client

proxy = xmlrpc.client.ServerProxy("http://127.0.0.1:6000/")

A = [
    [2, 0, 1],
    [3, 4, 2],
    [1, 2, 3]
]

B = [
    [1, 2, 3],
    [0, 1, 4],
    [5, 6, 0]
]

print("Sending matrices to RPC server...")

result = proxy.calculate(A, B)

print("\nResult Matrix from RPC Server:")

for row in result:
    print(row)
