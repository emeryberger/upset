import click
import math
import multiprocessing as mp
from collections import Counter
from functools import partial
import random

#def expected_unique_shuffles(N, T):
#    return math.factorial(N) * (1 - (1 - 1 / math.factorial(N)) ** T)

def expected_unique_shuffles(N, T):
    """
    Calculate the expected number of unique shuffles when shuffling N items T times.
    
    Args:
    N (int): Number of items being shuffled
    T (int): Number of shuffle operations
    
    Returns:
    float: Expected number of unique shuffles
    """
    n_factorial = math.factorial(N)
   
    # The exact formula: N! * (1 - (1 - 1/N!)^T)
    probability = 1 - (1 - 1/n_factorial) ** T
    expected = n_factorial * probability
    
    return expected


def shannon_entropy(data):
    """
    Calculates the Shannon entropy of a sequence.

    Args:
        data: A sequence of hashable items (e.g., string, list).

    Returns:
        The Shannon entropy of the sequence in bits.
    """
    if not data:
        return 0
    counts = Counter(data)
    probabilities = [float(c) / len(data) for c in counts.values()]
    entropy = -sum(p * math.log2(p) for p in probabilities if p > 0)
    return entropy # / math.log(sum(1 for p in probabilities if p > 0))

class MyObj:
    def __init__(self, name):
        self.name = name
    # No __hash__ override, so the default identity-based hashing is used.

def process_and_write(trial_num, output_file, N):
    objs = [MyObj(f"obj_{i}") for i in range(N)]
    obj_set = set(objs)
    l = list(o.name for o in obj_set)
    # random.shuffle(l) # FIXME

    with open(output_file, 'a') as f:
        f.write(f"{l}\n")

def main():
    TRIALS = 200 # Replace with your desired number of trials
    N = 8        # Replace with your desired N
    
    output_file = "results.txt"
    import os
    try:
        os.remove(output_file)
    except FileNotFoundError:
        pass

    # Create a pool of processes
    with mp.Pool() as pool:
        # Create a partial function with fixed arguments
        process_func = partial(process_and_write, 
                             output_file=output_file,
                             N=N)
        
        # Map the function to trial numbers
        pool.map(process_func, range(TRIALS))

    # Now read them back in and compute over them.
    with open(output_file, "r") as f:
        item_str = f.read()
        items = item_str.split('\n')
        items.pop()

        print(f"Percentage of duplicate orderings: {100 - (len(set(items)) * 100 / len(items))}%")
        print(f"  (expected: {100*(TRIALS-expected_unique_shuffles(N, TRIALS))/TRIALS:2.3}%)")
        print(f"Shannon entropy (number of bits): {shannon_entropy(items)}")

if __name__ == '__main__':
    main()

