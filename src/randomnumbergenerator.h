// -*- C++ -*-

/**
 * @file   randomnumbergenerator.h
 * @brief  A generic interface to random number generators.
 * @author Emery Berger <http://www.cs.umass.edu/~emery>
 * @note   Copyright (C) 2005 by Emery Berger, University of Massachusetts Amherst.
 */

#ifndef DH_RANDOMNUMBERGENERATOR_H
#define DH_RANDOMNUMBERGENERATOR_H

#include <random>

//#include "mwc64.h"
//#include "realrandomvalue.h"

class RandomNumberGenerator {
public:

  RandomNumberGenerator()
    : gen(rd())
  {
  }

  inline unsigned long next (void) {
    return distrib(gen);
  }

private:
  
  std::random_device rd;  // a seed source for the random number engine
  std::mt19937 gen; // mersenne_twister_engine seeded with rd()
  std::uniform_int_distribution<unsigned long> distrib;

};

#endif
