#ifndef _GNU_SOURCE
#define _GNU_SOURCE
#endif

#include <stdlib.h>
#include <dlfcn.h>

#if defined(__APPLE__)

// We will use Mach-O interposition so it's safe to just use malloc heap

class GlobalMallocHeap : public MallocHeap {};

#elif defined(__GNUC__) && !defined(__SVR4)

extern "C" {
  void * kmalloc(size_t);
  void kfree(void *);
  void * kcalloc(size_t, size_t);
  void * krealloc(void *, size_t);
  size_t kmalloc_usable_size(void *);
}

#include "kmalloc.c"

class GlobalMallocHeap : public MallocHeap {
public:
  
  //  enum { Alignment = MallocInfo::Alignment };
  
  GlobalMallocHeap()
  {
  }

  void *malloc(size_t size) {
    return real_malloc(size);
  }
  
  void free(void *ptr) {
    real_free(ptr);
  }

  void *calloc(size_t nmemb, size_t size) {
    void *ptr = real_calloc(nmemb, size);
    return ptr;
  }

  void *realloc(void *ptr, size_t size) {
    void *new_ptr = real_realloc(ptr, size);
    return new_ptr;
  }

  size_t getSize(void * ptr) {
    return real_getsize(ptr);
  }
  
private:

  typedef void *(*malloc_fn)(size_t);
  typedef void (*free_fn)(void *);
  typedef void *(*calloc_fn)(size_t, size_t);
  typedef void *(*realloc_fn)(void *, size_t);
  typedef size_t (*getsize_fn)(void *);
  
  malloc_fn real_malloc = kmalloc;
  free_fn real_free = kfree;
  calloc_fn real_calloc = kcalloc;
  realloc_fn real_realloc = krealloc;
  getsize_fn real_getsize = kmalloc_usable_size;
};

#endif

