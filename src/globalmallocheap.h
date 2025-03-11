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

#include <malloc.h>

extern "C" {
  void* __libc_malloc(size_t);
  void  __libc_free(void*);
  void* __libc_realloc(void*, size_t);
  void * __libc_calloc (size_t n, size_t elem_size);
}

class GlobalMallocHeap : public MallocHeap {
public:
  
  GlobalMallocHeap()
  {
  }

  void *malloc(size_t size) {
    return __libc_malloc(size);
  }
  
  void free(void *ptr) {
    __libc_free(ptr);
  }

  void *calloc(size_t nmemb, size_t size) {
    return __libc_calloc(nmemb, size);
  }

  void *realloc(void *ptr, size_t size) {
    return __libc_realloc(ptr, size);
  }

  size_t getSize(void * ptr) {
    typedef size_t (*getsize_fn)(void *);
    static getsize_fn real_getsize = (getsize_fn) nullptr;
    if (!real_getsize) {
      real_getsize = (getsize_fn) dlsym(RTLD_NEXT, "malloc_usable_size");
    }
    return real_getsize(ptr);
  }

};

#endif

