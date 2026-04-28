#include <stdio.h>
#include <time.h>


#define MAX_N 20
#define MAX_K 10

double min_sum_sq = 1e18;
int min_assignment[MAX_N];

void evaluate(int n, int k, int set[], int current_assignment[]) {
  double bucket_sums[k];

  // 1. Initialize sums to 0
  for (int i = 0; i < k; i++)
    bucket_sums[i] = 0;

  // 2. Sum the record values for each bucket
  for (int i = 0; i < n; i++) {
    int target_bucket = current_assignment[i];
    bucket_sums[target_bucket] += set[i];
  }

  // 3. Calculate Sum of Squares
  double current_fS = 0;
  for (int i = 0; i < k; i++) {
    current_fS += (bucket_sums[i] * bucket_sums[i]);
  }

  // 4. Update the Leaderboard
  if (current_fS < min_sum_sq) {
    min_sum_sq = current_fS;
    for (int i = 0; i < n; i++) {
      min_assignment[i] = current_assignment[i];
    }
  }
}

void solve(int index, int n, int k, int set[], int current_assignment[]) {
  if (index == n) {
    evaluate(n, k, set, current_assignment);
    return;
  }

  for (int i = 0; i < k; i++) {
    current_assignment[index] = i;
    solve(index + 1, n, k, set, current_assignment);
  }
}
int main() {
  int n, k;
  int set[MAX_N];
  int current_assignment[MAX_N];

  printf("Enter number of elements (n): ");
  scanf("%d", &n);
  printf("Enter elements: ");
  for (int i = 0; i < n; i++)
    scanf("%d", &set[i]);
  printf("Enter number of subsets (k): ");
  scanf("%d", &k);

  struct timespec start, end;
  clock_gettime(CLOCK_MONOTONIC, &start);

  solve(0, n, k, set, current_assignment);

  clock_gettime(CLOCK_MONOTONIC, &end);
  double time_taken = (end.tv_sec - start.tv_sec) + (end.tv_nsec - start.tv_nsec) / 1e9;

  printf("Minimum Sum of Square: %lf \n", min_sum_sq);
  for (int i = 0; i < n; i++) {
    printf("Element %d -> Bucket %d\n", set[i], min_assignment[i]);
  }
  printf("\nExecution time: %lf seconds\n", time_taken);

  return 0;
}