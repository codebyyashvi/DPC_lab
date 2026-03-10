#include <stdio.h>
#include <stdlib.h>
#include <omp.h>
#include <time.h>
#include <string.h>

#define N 12

int isSorted(int arr[]) {
    for (int i = 0; i < N - 1; i++) {
        if (arr[i] > arr[i + 1])
            return 0;
    }
    return 1;
}

void shuffle(int arr[]) {
    for (int i = N - 1; i > 0; i--) {
        int j = rand() % (i + 1);
        int temp = arr[i];
        arr[i] = arr[j];
        arr[j] = temp;
    }
}

void printArray(int arr[]) {
    for (int i = 0; i < N; i++)
        printf("%d ", arr[i]);
    printf("\n");
}

double parallelBogo(int original[], int threads,
                    long long *totalShuffles,
                    int finalResult[],
                    int *winnerThread) {

    int found = 0;
    *totalShuffles = 0;

    double start = omp_get_wtime();

    #pragma omp parallel num_threads(threads)
    {
        int localArr[N];
        memcpy(localArr, original, sizeof(int) * N);

        unsigned int seed = time(NULL) ^ omp_get_thread_num();
        srand(seed);

        while (!found) {

            if (isSorted(localArr)) {
                #pragma omp critical
                {
                    if (!found) {
                        memcpy(finalResult, localArr, sizeof(int) * N);
                        found = 1;
                        *winnerThread = omp_get_thread_num();
                    }
                }
            }

            shuffle(localArr);

            #pragma omp atomic
            (*totalShuffles)++;

            #pragma omp flush(found)
        }
    }

    return omp_get_wtime() - start;
}

int main() {

    int original[N];

    for (int i = 0; i < N; i++)
        original[i] = i + 1;

    srand(time(NULL));
    shuffle(original);

    /* ---- Sample Array ---- */
    printf("Sample Array: ");
    printArray(original);

    int threadList[3] = {2, 4, 8};
    double times[3];
    long long shuffles[3];

    for (int i = 0; i < 3; i++) {

        int sorted[N];
        int winner;

        times[i] = parallelBogo(original, threadList[i],
                                &shuffles[i], sorted, &winner);

        if (threadList[i] == 4) {
            printf("\nParallel Run (Threads = 4):\n");
            printf("Thread %d found the sorted array!\n", winner);
            printf("Sorted Array: ");
            printArray(sorted);
            printf("Time Taken: %.3f sec\n", times[i]);
            printf("Total Shuffles: %lld\n\n", shuffles[i]);
        }
    }

    printf("Summary Table:\n");
    printf("Threads   Time(sec)   Shuffles   Speedup\n");

    double baseTime = times[0]; 

    for (int i = 0; i < 3; i++) {
        printf("%d        %.3f      %lld      %.2f\n",
               threadList[i],
               times[i],
               shuffles[i],
               baseTime / times[i]);
    }

    return 0;
}
