// -*- C++ -*-

#ifndef DH_SHUFFLEHEAP_H
#define DH_SHUFFLEHEAP_H

#include <algorithm>
#include <array>

#include <stdlib.h>

#include "modulo.h"
#include "randomnumbergenerator.h"

#include <printf.h>

template <int NObjects,
	  class SuperHeap>
class ShuffleHeap : public SuperHeap {
public:

  ShuffleHeap()
    : _reqSize (0)
  {
  }


  inline void * malloc (size_t sz) {
    if (_reqSize == 0) {
      fillBuffer(sz);
    }
    assert (sz <= _reqSize);
    // Get an item from the superheap and swap it with a
    // randomly-chosen object from the array. This is one step of an
    // in-place Fisher-Yates shuffle.
    void * ptr = SuperHeap::malloc (_reqSize);
    int j = modulo<NObjects>(_rng.next());
    swap(_buffer[j], ptr);
    return ptr;
  }


  inline void free (void * ptr) {
    // Choose a random item and evict it to the superheap,
    // replacing it with the one we are now freeing.
    int j = modulo<NObjects>(_rng.next());
    swap(_buffer[j], ptr);
    SuperHeap::free (ptr);
  }

 
private:

  void fillBuffer(size_t sz) {
    // Get an object from the superheap and see how big it really is;
    // fill the buffer and then use that request size going forwards.
    void * ptr = SuperHeap::malloc(sz);
    size_t s   = SuperHeap::getSize(ptr);
    SuperHeap::free (ptr);
    _reqSize = s;
    assert(sz <= s);
    fill(_reqSize);
  }
  
  void fill (size_t sz) {
    // Fill up the buffer from the superheap. We'll allocate randomly from this buffer.
    for (int i = 0; i < NObjects; i++) {
      _buffer[i] = SuperHeap::malloc (sz);
    }
  }

  /// Object request size
  size_t _reqSize;

  /// The random number generator, used for shuffling and random selection.
  RandomNumberGenerator _rng;

  /// The buffer used to hold shuffled objects for heap requests.
  std::array<void *, NObjects> 	_buffer;

};


#endif
