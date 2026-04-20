from mpi4py import MPI
import random

def main():
    """
    Distributed Banking System using MPI
    - Master node (Rank 0): Coordinates and aggregates data
    - Branch nodes (Rank > 0): Process transactions in parallel
    """
    # Initialize the MPI communicator
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()  # The ID of the current process
    size = comm.Get_size()  # Total number of processes

    if size < 2:
        if rank == 0:
            print("Error: Please run with at least 2 processes (1 Master, 1+ Branches).")
            print("Example: mpiexec -n 4 python mpi_banking.py")
        return

    local_daily_deposit = 0.0

    if rank != 0:
        # Simulate local branch processing 100 transactions in parallel
        for _ in range(100):
            local_daily_deposit += random.uniform(10.0, 500.0)

        print(f"[Branch {rank}] Processed 100 transactions. Net deposit: ${local_daily_deposit:.2f}")

    total_national_deposit = comm.reduce(local_daily_deposit, op=MPI.SUM, root=0)

    # Master node prints the final aggregated result
    if rank == 0:
        print("\n" + "=" * 60)
        print("[Central Bank - Master Node 0]")
        print(f"Total National Deposits collected from {size - 1} branches:")
        print(f"Total: ${total_national_deposit:.2f}")
        print("=" * 60 + "\n")


if __name__ == "__main__":
    main()