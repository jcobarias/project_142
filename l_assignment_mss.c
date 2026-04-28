#include <stdio.h>
#include <stdlib.h>

#define MAX_N 20
#define MAX_K 10
double min_sum_sq = 1e18;
int min_assignment[MAX_N];

int descending_compare(const void *a, const void *b) {
  int val_a = *(int *)a;
  int val_b = *(int *)b;

  if (val_a > val_b)
    return -1;
  else if (val_a < val_b)
    return 1;
  else
    return 0;
}
int find_lightest_bucket(int bucket_sums[], int k) {
  int lightest = bucket_sums[0];
  int index = 0;

  for (int i = 1; i < k; i++) {
    if (bucket_sums[i] < lightest) {
      lightest = bucket_sums[i];
      index = i;
    }
  }
  return index;
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

  int bucket_sums[k];

  for (int i = 0; i < k; i++)
    bucket_sums[i] = 0;

  qsort(set, n, sizeof(int), descending_compare);

  int alt = 0;
  for (int i = 0; i < k; i++) {
    bucket_sums[alt] = set[i];
    current_assignment[i] = alt;
    if (alt == k - 1)
      alt = 0;
    else
      alt++;
  }

  for (int i = k; i < n; i++) {
    int index = find_lightest_bucket(bucket_sums, k);
    bucket_sums[index] += set[i];
    current_assignment[i] = index;
  }

  double min_fS = 0;
  for (int i = 0; i < k; i++) {
    min_fS += (bucket_sums[i] * bucket_sums[i]);
  }

  printf("Minimum Sum of Square: %lf \n", min_fS);
  printf("\nAssignment (which bucket each sorted element went to):\n");
  for (int i = 0; i < n; i++) {
    printf("Element %d -> Bucket %d\n", set[i], current_assignment[i]);
  }

  return 0;
}