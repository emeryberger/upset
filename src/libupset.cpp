// The undef below ensures that any pthread_* calls get strong
// linkage.  Otherwise, our versions here won't replace them.  It is
// IMPERATIVE that this line appear before any files get included.

#undef __GXX_WEAK__ 

#include <stdlib.h>
#include <new>
#include <heaplayers>

#include "shuffleheap.h"
#include "globalmallocheap.h"
#include <printf.h>

#include <unistd.h>

// For use by the replacement printf routines (see
// https://github.com/mpaland/printf)
extern "C" void _putchar(char ch) { ::write(1, (void *)&ch, 1); }

template <class S>
class SuperWrapper : public S {
public:
  typedef S Super;
};

class SmallShuffler : public SuperWrapper<KingsleyHeap<ShuffleHeap<32, GlobalMallocHeap>, GlobalMallocHeap>> {
public:
  void * malloc(size_t sz) {
    auto ptr = Super::malloc(sz);
    return ptr;
  }
};


class Shuffler : public ANSIWrapper<
    LockedHeap<PosixLockType,
	       //	       SmallShuffler>> {};
	       HybridHeap<65536,
			  SmallShuffler,
			  GlobalMallocHeap>>> {};

class TheCustomHeapType : public Shuffler {};

inline static TheCustomHeapType * getCustomHeap (void) {
  static char buf[sizeof(TheCustomHeapType)];
  static TheCustomHeapType * _theCustomHeap = 
    new (buf) TheCustomHeapType;
  return _theCustomHeap;
}

#if defined(_WIN32)
#pragma warning(disable:4273)
#endif

// Heap-Layers
#include "wrappers/generic-memalign.cpp"

extern "C" {

  void * xxmalloc (size_t sz) {
    auto ptr = getCustomHeap()->malloc (sz);
    return ptr;
  }

  void xxfree (void * ptr) {
    getCustomHeap()->free (ptr);
  }

  void * xxmemalign(size_t alignment, size_t sz) {
    return generic_xxmemalign(alignment, sz);
  }
  
  size_t xxmalloc_usable_size (void * ptr) {
    return getCustomHeap()->getSize (ptr);
  }

  void xxmalloc_lock() {
    getCustomHeap()->lock();
  }

  void xxmalloc_unlock() {
    getCustomHeap()->unlock();
  }

}
