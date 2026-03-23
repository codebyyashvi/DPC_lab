 gcc hello_mpi.c -o hello_mpi.exe -I"C:\Program Files (x86)\Microsoft SDKs\MPI\Include" -L"C:\Program Files (x86)\Microsoft SDKs\MPI\Lib\x64" -lmsmpi
 mpiexec -n 4 .\hello_mpi.exe