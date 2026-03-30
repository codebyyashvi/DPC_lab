#include <mpi.h>
#include <iostream>
using namespace std;

typedef long long ll;

ll modExp(ll base, ll exp, ll mod) {
    ll res = 1;
    base %= mod;
    while (exp > 0) {
        if (exp & 1) res = (res * base) % mod;
        base = (base * base) % mod;
        exp >>= 1;
    }
    return res;
}

ll modInverse(ll a, ll mod) {
    ll m0 = mod, t, q;
    ll x0 = 0, x1 = 1;

    if (mod == 1) return 0;

    while (a > 1) {
        q = a / mod;
        t = mod;
        mod = a % mod, a = t;
        t = x0;
        x0 = x1 - q * x0;
        x1 = t;
    }

    if (x1 < 0) x1 += m0;
    return x1;
}

ll grinder(ll seed, ll m, ll a, ll mod, ll N) {
    ll mN = modExp(m, N, mod);

    if (m == 1) {
        return (seed + N * a) % mod;
    }

    ll inv = modInverse(m - 1, mod);

    ll part1 = (seed * mN) % mod;
    ll part2 = ((mN - 1 + mod) % mod * inv) % mod;
    part2 = (part2 * a) % mod;

    return (part1 + part2) % mod;
}

int main(int argc, char** argv) {
    MPI_Init(&argc, &argv);

    int rank, size;
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    if (size != 2) {
        if (rank == 0)
            cout << "Run with exactly 2 processes.\n";
        MPI_Finalize();
        return 0;
    }

    ll A = 1060;  
    ll B = 1067;

    ll N = 2000000000LL;

    double start = MPI_Wtime();

    if (rank == 0) {

        ll alpha1 = grinder(A, 31, 17, 9973, N);
        ll alpha2 = grinder(alpha1, 37, 11, 9973, N);
        ll alpha = (alpha1 + alpha2) % 9973;

        cout << "Alpha: " << alpha << endl;

        MPI_Send(&alpha, 1, MPI_LONG_LONG, 1, 0, MPI_COMM_WORLD);

        ll beta;
        MPI_Recv(&beta, 1, MPI_LONG_LONG, 1, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);

        cout << "Beta: " << beta << endl;

        ll verify = grinder(alpha + beta, 7, 3, 101, N);

        ll R = grinder(alpha * beta + A + B, 13, 7, 9973, N);
        ll password = R % 10000;

        double end = MPI_Wtime();

        cout << "Verify: " << verify << endl;
        cout << "Password: " << password << endl;
        cout << "Time: " << (end - start) << " seconds\n";
    }
    else if (rank == 1) {

        ll alpha;
        MPI_Recv(&alpha, 1, MPI_LONG_LONG, 0, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);

        ll beta1 = grinder(alpha, B, 13, 9973, N);
        ll beta2 = grinder(beta1, 41, 19, 9973, N);
        ll beta = (beta1 + beta2) % 9973;

        cout << "Alpha (received): " << alpha << endl;
        cout << "Beta (computed): " << beta << endl;

        MPI_Send(&beta, 1, MPI_LONG_LONG, 0, 0, MPI_COMM_WORLD);

        ll verify = grinder(alpha + beta, 7, 3, 101, N);

        cout << "Verify (Process 1): " << verify << endl;
    }

    MPI_Finalize();
    return 0;
}