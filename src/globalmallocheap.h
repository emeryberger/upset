#ifndef _GNU_SOURCE
#define _GNU_SOURCE
#endif

#include <stdlib.h>
#include <dlfcn.h>

#if defined(__APPLE__)

// We will use Mach-O interposition so it's safe to just use malloc heap

class GlobalMallocHeap : public MallocHeap {};

#elif defined(__GNUC__) && !defined(__SVR4)

class GlobalMallocHeap : public MallocHeap {
public:
  
  //  enum { Alignment = MallocInfo::Alignment };
  
  GlobalMallocHeap()
  {
    init();
  }

  void *malloc(size_t size) {
    if (!real_malloc) {
      init();
    }
    return real_malloc(size);
  }
  
  void free(void *ptr) {
    if (!real_free) {
      init();
    }
    real_free(ptr);
  }

  void *calloc(size_t nmemb, size_t size) {
    if (!real_calloc) {
      init();
    }
    void *ptr = real_calloc(nmemb, size);
    return ptr;
  }

  void *realloc(void *ptr, size_t size) {
    if (!real_realloc) {
      init();
    }
    void *new_ptr = real_realloc(ptr, size);
    return new_ptr;
  }

  size_t getSize(void * ptr) {
    if (!real_getsize) {
      init();
    }
    return real_getsize(ptr);
  }
  
private:

  typedef void *(*malloc_fn)(size_t);
  typedef void (*free_fn)(void *);
  typedef void *(*calloc_fn)(size_t, size_t);
  typedef void *(*realloc_fn)(void *, size_t);
  typedef size_t (*getsize_fn)(void *);
  
  malloc_fn real_malloc = (malloc_fn) nullptr;
  free_fn real_free = (free_fn) nullptr;
  calloc_fn real_calloc = (calloc_fn) nullptr;
  realloc_fn real_realloc = (realloc_fn) nullptr;
  getsize_fn real_getsize = (getsize_fn) nullptr;
  
  void init() {
    real_malloc = (malloc_fn) dlsym(RTLD_NEXT, "malloc");
    real_free = (free_fn) dlsym(RTLD_NEXT, "free");
    real_calloc = (calloc_fn) dlsym(RTLD_NEXT, "calloc");
    real_realloc = (realloc_fn) dlsym(RTLD_NEXT, "realloc");
    real_getsize = (getsize_fn) dlsym(RTLD_NEXT, "malloc_usable_size");
  }

};

#endif

