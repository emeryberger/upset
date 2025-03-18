import click
import math
import multiprocessing as mp
import random

from collections import Counter
from decimal import Decimal, getcontext
from functools import partial


def expected_unique_shuffles(N, T):
    """
    Calculate the expected number of unique shuffles when shuffling N items T times.
    Uses logarithms and Decimal for numerical stability with large numbers.
    
    Args:
    N (int): Number of items being shuffled
    T (int): Number of times shuffling
    
    Returns:
    float: Expected number of unique shuffles
    """
    if N < 0 or T < 0:
        raise ValueError("N and T must be non-negative")
    
    if N == 0 or T == 0:
        return 0
    
    if N == 1:
        return 1

    # Set precision for Decimal calculations
    getcontext().prec = 100

    # Calculate log(N!)
    log_n_factorial = sum(math.log(i) for i in range(1, N + 1))

    # For large N, (1 - 1/N!)^T can be approximated using exp(-T/N!)
    # This is more numerically stable than the direct calculation
    if N > 15:  # threshold where we switch to approximation
        # Using log space to handle large numbers
        ratio = -Decimal(T) * Decimal(math.exp(-log_n_factorial))
        probability = Decimal(1) - Decimal(ratio.exp())
        result = float(probability * Decimal(math.exp(log_n_factorial)))
    else:
        # For smaller N, we can use the direct calculation
        n_factorial = math.factorial(N)
        probability = 1 - (1 - 1/n_factorial) ** T
        result = n_factorial * probability

    result = result if result <= T else T
    return result



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
    # Force a lot of allocations to warm up the heap
    objs = [MyObj(f"obj_{i}") for i in range(N * N)]
    # Now just allocate N objects
    objs = [MyObj(f"obj_{i}") for i in range(N)]
    obj_set = set(objs)
    l = list(o.name for o in obj_set)
    # random.shuffle(l) # FIXME

    with open(output_file, 'a') as f:
        f.write(f"{l}\n")

@click.command(context_settings={"allow_extra_args": True, "ignore_unknown_options": True})
@click.option('--n', type=int, default=20)
@click.option('--trials', type=int, default=200)
def main(n, trials):
    
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
                             N=n)
        
        # Map the function to trial numbers
        pool.map(process_func, range(trials))

    # Now read them back in and compute over them.
    with open(output_file, "r") as f:
        item_str = f.read()
        items = item_str.split('\n')
        items.pop()

        print(f"Percentage of duplicate orderings: {100 - (len(set(items)) * 100 / len(items))}%")
        print(f"  (expected: {100*(trials-expected_unique_shuffles(n, trials))/trials:2.3}%)")
        print(f"Shannon entropy (number of bits): {shannon_entropy(items)}")

if __name__ == '__main__':
    main()

