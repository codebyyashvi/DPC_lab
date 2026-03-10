#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <omp.h>

static long long solve_row(uint64_t cols, uint64_t diag1, uint64_t diag2, uint64_t all_cols) {
	if (cols == all_cols) {
		return 1;
	}

	long long count = 0;
	uint64_t available = all_cols & ~(cols | diag1 | diag2);

	while (available) {
		uint64_t pos = available & (~available + 1ULL);
		available -= pos;
		count += solve_row(cols | pos, (diag1 | pos) << 1, (diag2 | pos) >> 1, all_cols);
	}

	return count;
}

int main(int argc, char *argv[]) {
	int n;

	if (argc > 1) {
		n = atoi(argv[1]);
	} else {
		printf("Enter board size N: ");
		if (scanf("%d", &n) != 1) {
			fprintf(stderr, "Invalid input.\n");
			return 1;
		}
	}

	if (n < 1 || n > 32) {
		fprintf(stderr, "Please provide N in the range 1 to 32.\n");
		return 1;
	}

	uint64_t all_cols = (1ULL << n) - 1ULL;
	long long total_solutions = 0;

	double start = omp_get_wtime();

	#pragma omp parallel for reduction(+:total_solutions) schedule(dynamic)
	for (int col = 0; col < n; col++) {
		uint64_t pos = 1ULL << col;
		total_solutions += solve_row(pos, pos << 1, pos >> 1, all_cols);
	}

	double end = omp_get_wtime();

	printf("N = %d\n", n);
	printf("Total solutions = %lld\n", total_solutions);
	printf("Threads used = %d\n", omp_get_max_threads());
	printf("Execution time = %.6f seconds\n", end - start);

	return 0;
}