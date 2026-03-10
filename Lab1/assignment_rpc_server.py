from xmlrpc.server import SimpleXMLRPCServer

def multiply_matrices(A, B):
    rowsA = len(A)
    colsA = len(A[0])
    rowsB = len(B)
    colsB = len(B[0])

    if colsA != rowsB:
        return "Matrix multiplication not possible"

    result = [[0 for _ in range(colsB)] for _ in range(rowsA)]

    for i in range(rowsA):
        for j in range(colsB):
            for k in range(colsA):
                result[i][j] += A[i][k] * B[k][j]

    return result


def calculate(A, B):
    return multiply_matrices(A, B)


server = SimpleXMLRPCServer(("0.0.0.0", 6000))
print("RPC Matrix Multiplication Server running...")

server.register_function(calculate, "calculate")

server.serve_forever()
