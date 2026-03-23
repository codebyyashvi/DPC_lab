#include <mpi.h>
#include <stdio.h>

int main(int argc, char** argv) {
    int rank, size;

    // Initialize MPI
    MPI_Init(&argc, &argv);

    // Get process ID (rank)
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);

    // Get total number of processes
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    printf("Hello from process %d out of %d processes\n", rank, size);

    // Finalize MPI
    MPI_Finalize();

    return 0;
}