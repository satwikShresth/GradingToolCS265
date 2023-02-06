#include <dlfcn.h>
#include <stdio.h>
#include <stdlib.h>
#include <signal.h>
#include <unistd.h>

void segfault_handler(int signal) {
  printf("Caught segmentation fault\n");
  _exit(1);
}

int main(int argc, char** argv) {
  void *handle;
  int* (*split)(int[], int, int);
  char *error;

  handle = dlopen(argv[1], RTLD_LAZY);
  if (!handle) {
    fprintf(stderr, "%s\n", dlerror());
    exit(1);
  }

  int* (*split_func)(int[], *int, *int) = dlsym(handle, "split");
  if (!split_func)  {
    fprintf(stderr, "%s\n", error);
    exit(1);
  }

  struct sigaction sa;
  sa.sa_handler = segfault_handler;
  sigemptyset(&sa.sa_mask);
  sa.sa_flags = 0;
  
  if (sigaction(SIGSEGV, &sa, NULL) == -1) {
    perror("Error installing signal handler");
    return 1;
  }
  
  int a[10] = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};
  int low = 0;
  int high = 9;
  int* middle = split_func(a, low, high);
  printf("%d\n", *middle);

  dlclose(handle);

  return 0;
}