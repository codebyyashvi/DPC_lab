#include <stdio.h>
#include <stdlib.h>
#include <omp.h>

#define N 8

int isSafe(int board[N], int row, int col) {
    for (int i = 0; i < row; i++) {
        if (board[i] == col){
            return 0;
        }
        if (abs(board[i]-col)==abs(i-row)){
            return 0;
        }
    }
    return 1;
}

int solveNQueens(int board[N], int row) {
    if (row == N){
        return 1;
    }
    int count = 0;
    for (int col = 0; col < N; col++) {
        if (isSafe(board, row, col)) {
            board[row] = col;
            count += solveNQueens(board, row + 1);
        }
    }
    return count;
}

int main() {
    int totalSolutions = 0;
    double start, end;
    start = omp_get_wtime();
    #pragma omp parallel for reduction(+:totalSolutions)
    for (int col = 0; col < N; col++) {
        int board[N];
        board[0] = col;
        totalSolutions += solveNQueens(board, 1);
    }
    end = omp_get_wtime();
    printf("Board Size (N=%d)\n", N);
    printf("Total Number of valid solutions: %d\n", totalSolutions);
    printf("Execution Time: %f seconds\n", end - start);
    return 0;
}