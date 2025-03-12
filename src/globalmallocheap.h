#ifndef _GNU_SOURCE
#define _GNU_SOURCE
#endif

#include <stdlib.h>
#include <dlfcn.h>

#if defined(__APPLE__)

// We will use Mach-O interposition so it's safe to just use malloc heap

class GlobalMallocHeap : public MallocHeap {
public:
  bool initialized() const { return true; }
};

#elif defined(__GNUC__) && !defined(__SVR4)

#define MALLOC_PREFIX(x) dl##x

extern "C" {
  void * MALLOC_PREFIX(malloc)(size_t);
  void MALLOC_PREFIX(free)(void *);
  void * MALLOC_PREFIX(calloc)(size_t, size_t);
  void * MALLOC_PREFIX(realloc)(void *, size_t);
  size_t MALLOC_PREFIX(malloc_usable_size)(void *);
}

class GlobalMallocHeap : public MallocHeap {
public:
  
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
  
  malloc_fn real_malloc = MALLOC_PREFIX(malloc);
  free_fn real_free = MALLOC_PREFIX(free);
  calloc_fn real_calloc = MALLOC_PREFIX(calloc);
  realloc_fn real_realloc = MALLOC_PREFIX(realloc);
  getsize_fn real_getsize = MALLOC_PREFIX(malloc_usable_size);
};

#endif

