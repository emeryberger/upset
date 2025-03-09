// -*- C++ -*-

#ifndef DH_SHUFFLEHEAP_H
#define DH_SHUFFLEHEAP_H

#include <algorithm>
#include <array>

#include <stdlib.h>

#include "modulo.h"
#include "randomnumbergenerator.h"

#define FIXED_SIZE 0

template <int NObjects,

#if FIXED_SIZE
	  size_t Size,
#endif

	  class SuperHeap>
class ShuffleHeap : public SuperHeap {
public:

  ShuffleHeap()
    : _reqSize (0)
  {
#if FIXED_SIZE
    fill (Size);
#endif
  }


  inline void * malloc (size_t sz) {
#if FIXED_SIZE
    assert (sz <= Size);
    reqSize = Size;
#else
    if (_reqSize == 0) {
      // Get an object from the superheap and see how big it really is;
      // fill the buffer and then use that request size going forwards.
      void * ptr = SuperHeap::malloc(sz);
      size_t s   = SuperHeap::getSize(ptr);
      SuperHeap::free (ptr);
      _reqSize = s;
      assert (sz <= s);
      fill (_reqSize);
    }
#endif
    assert (sz <= _reqSize);
    // Get an item from the superheap and swap it with a
    // randomly-chosen object from the array. This is one step of an
    // in-place Fisher-Yates shuffle.
    void * ptr = SuperHeap::malloc (_reqSize);
    int j = modulo<NObjects>(_rng.next());
    swap (_buffer[j], ptr);
    return ptr;
  }


  inline void free (void * ptr) {
    // Choose a random item and evict it to the superheap,
    // replacing it with the one we are now freeing.
    int j = modulo<NObjects>(_rng.next());
    swap (_buffer[j], ptr);
    SuperHeap::free (ptr);
  }

 
private:

  void fill (size_t sz) {
    // Fill up the buffer from the superheap. We'll allocate randomly from this buffer.
    for (int i = 0; i < NObjects; i++) {
      _buffer[i] = SuperHeap::malloc (sz);
    }
#if 1
    // Now shuffle it (Fisher-Yates).
    for (int i = NObjects - 1; i >= 1; i--) {
      // Pick a random integer, 0 ≤ j ≤ i, and swap with item i.
      int j = _rng.next() % (i+1);
      swap (_buffer[i], _buffer[j]);
    }
#endif
  }

  /// Object request size
  size_t _reqSize;

  /// The random number generator, used for shuffling and random selection.
  RandomNumberGenerator 	_rng;

  /// The buffer used to hold shuffled objects for heap requests.
  std::array<void *, NObjects> 	_buffer;

};


#endif
