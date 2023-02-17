#include <dlfcn.h>
#include <stdio.h>
#include <stdlib.h>
#include <signal.h>
#include <unistd.h>
#include <stdbool.h>

#define N 10


void segfaultHandler(int signal);
bool is_same(int arr1[], int arr2[], int n);
void testQuickSort(void *handle);



int main(int argc, char** argv) {
  void *handle;

  handle = dlopen(argv[1], RTLD_LAZY);
  if (!handle) {
    fprintf(stderr, "%s\n", dlerror());
    exit(1);
  }

  struct sigaction sa;
  sa.sa_handler = segfaultHandler;
  sigemptyset(&sa.sa_mask);
  sa.sa_flags = 0;
  
  if (sigaction(SIGSEGV, &sa, NULL) == -1) {
    perror("Error installing signal handler");
    return 1;
  }
  testQuickSort(handle);
  dlclose(handle);
  return 0;
}


void segfaultHandler(int signal) {
  printf("Caught Segmentation Fault");
  exit(0);
}


void testQuickSort(void *handle){
  
  int points=0,i;
  char *error;

  void (*quicksort_func)(int*,int*,int*) = dlsym(handle, "quicksort");
  if (!quicksort_func)  {
    fprintf(stderr, "%s\n", error);
    exit(0);
  }

  int testString_1[10]= {734, 896, 402, 977, 781, 671, 212, 163, 679, 502};
  int answerString_1[10]= {163, 212, 402, 502, 671, 679, 734, 781, 896, 977};
  quicksort_func(testString_1, &testString_1[0], &testString_1[9]);
  if (is_same(testString_1, answerString_1, 10)){
      printf("{\"1\":[");
    for (i=0; i<N; i++){
      if (i==0){
        printf("%d", testString_1[i]);
      }
      else{
        printf(",%d", testString_1[i]);
      }
    }
    printf("]}\n");
  }

  int testString_2[10]= {194, 732, 243, 952, 719, 812, 603, 541, 890, 910};
  int answerString_2[10]= {194, 243, 541, 603, 719, 732, 812, 890, 910, 952};
  quicksort_func(testString_2, &testString_2[0], &testString_2[9]);
  if (is_same(testString_2, answerString_2, 10)){
      printf("{\"2\":[");
    for (i=0; i<N; i++){
      if (i==0){
        printf("%d", testString_2[i]);
      }
      else{
        printf(",%d", testString_2[i]);
      }
    }
    printf("]}\n");
  }
  int testString_3[10]= {367, 991, 784, 546, 310, 165, 886, 969, 807, 527};
  int answerString_3[10]= {165, 310, 367, 527, 546, 784, 807, 886, 969, 991};
  quicksort_func(testString_3, &testString_3[0], &testString_3[9]);
  if (is_same(testString_3, answerString_3, 10)){
      printf("{\"3\":[");
    for (i=0; i<N; i++){
      if (i==0){
        printf("%d", answerString_3[i]);
      }
      else{
        printf(",%d", answerString_3[i]);
      }
    }
    printf("]}\n");
  }
  int testString_4[10]= {956, 879, 566, 793, 642, 623, 233, 474, 168, 713};
  int answerString_4[10]= {168, 233, 474, 566, 623, 642, 713, 793, 879, 956};
  quicksort_func(testString_4, &testString_4[0], &testString_4[9]);
  if (is_same(testString_4, answerString_4, 10)){
      printf("{\"4\":[");
    for (i=0; i<N; i++){
      if (i==0){
        printf("%d", testString_4[i]);
      }
      else{
        printf(",%d", testString_4[i]);
      }
    }
    printf("]}\n");
  }

  int testString_5[10]= {758, 191, 903, 443, 526, 986, 849, 598, 126, 660};
  int answerString_5[10]= {126, 191, 443, 526, 598, 660, 758, 849, 903, 986};
  quicksort_func(testString_5, &testString_5[0], &testString_5[9]);
  if (is_same(testString_5, answerString_5, 10)){
      printf("{\"5\":[");
    for (i=0; i<N; i++){
      if (i==0){
        printf("%d", answerString_5[i]);
      }
      else{
        printf(",%d", answerString_5[i]);
      }
    }
    printf("]}\n");
  }
}


bool is_same(int arr1[], int arr2[], int n) {
    for (int i = 0; i < n; i++) {
        if (arr1[i] != arr2[i]) {
            return true;
        }
    }
    return false;
}