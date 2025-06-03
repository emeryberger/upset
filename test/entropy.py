import click
import math
import multiprocessing as mp
import random
import click
import math
import random
import fcntl
import os
from functools import partial
from collections import Counter
from decimal import Decimal, getcontext
from itertools import combinations
import multiprocessing as mp


def init(lock):
    global mplock
    mplock = lock

from collections import Counter
from decimal import Decimal, getcontext
from functools import partial

def theoretical_expected_inversions(M, N):
    return (M * (M-1) * N * (N-1)) / 8


def count_inversions_between_lists(list1, list2):
    """
    Count inversions between two lists.
    An inversion occurs when elements i,j appear in different order in the two lists.
    """
    # Create a position map for the second list
    pos_map = {val: idx for idx, val in enumerate(list2)}
    
    inversions = 0
    n = len(list1)
    
    # For each pair of elements in list1, check if they're inverted in list2
    for i in range(n):
        for j in range(i + 1, n):
            # If element at position i comes after element at position j in list2,
            # it's an inversion
            if pos_map[list1[i]] > pos_map[list1[j]]:
                inversions += 1
                
    return inversions

def count_all_list_pair_inversions(lists):
    """
    Count inversions between all pairs of lists in the input.
    """
    total_inversions = 0
    m = len(lists)
    
    # Compare each pair of lists
    for i in range(m):
        for j in range(i + 1, m):
            inversions = count_inversions_between_lists(lists[i], lists[j])
            total_inversions += inversions
            
    return total_inversions


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
    # warm-up allocations
    # objs = [MyObj(f"obj_{i}") for i in range(N*N)]
    objs = [MyObj(f"obj_{i}") for i in range(N)]
    obj_set = set(objs)
    l = list(o.name for o in obj_set)
    # random.shuffle(l)

    global mplock
    with mplock:
        with open(output_file, 'a+') as f:
            f.write(f"{l}\n")
            f.flush()
            os.fsync(f.fileno())

            
def old_process_and_write(trial_num, output_file, N):
    # atomic append + file-lock guard
    if False: # with open(output_file, "a+") as f:
        # acquire an exclusive lock on the open file descriptor
        fcntl.flock(f.fileno(), fcntl.LOCK_EX)
        try:
            f.write(f"{l}\n")
            f.flush()
            os.fsync(f.fileno())
        finally:
            # release the lock
            fcntl.flock(f.fileno(), fcntl.LOCK_UN)

from decimal import Decimal, getcontext
from typing import List, Union
import numpy as np

def expected_trials_to_non_duplicate(p: List[Union[float, Decimal]], prec: int = 50) -> Decimal:
    """
    Compute the expected number of draws (with replacement) until
    you draw a value you have NOT seen before (i.e., first "new" outcome),
    given probabilities p_i for each of N choices.

    Formula:
      E[T] = 1 + sum_{i=1}^N ( p_i / (1 - p_i) )
    because with probability p_i you start with i, then wait Geom(1-p_i) for a different.
    """
    # Use Decimal for precision if any p_i are Decimal
    getcontext().prec = prec
    # Convert all p_i to Decimal
    p_dec = [Decimal(pi) for pi in p]

    result = Decimal(1)  # first draw is always "new"
    for pi in p_dec:
        if pi == 1:
            # If one type has probability 1, you'll never see a different type
            return Decimal('Infinity')
        result += pi / (Decimal(1) - pi)
    return result


from itertools import combinations
from scipy.stats import kendalltau

import numpy as np


from itertools import combinations
from typing import List, Dict

def kendall_tau_distance(p1: List[str], p2: List[str]) -> int:
    """Compute the Kendall tau distance (number of pairwise inversions) between two permutations of strings."""
    n: int = len(p1)
    
    # Build inverse map for p2
    pos_map: Dict[str, int] = {val: idx for idx, val in enumerate(p2)}
    mapped: List[int] = [pos_map[val] for val in p1]

    # Count inversions in mapped list
    inv_count: int = 0
    for i in range(n):
        for j in range(i + 1, n):
            if mapped[i] > mapped[j]:
                inv_count += 1
    return inv_count

def mean_pairwise_kendall_tau(perms: List[List[str]]) -> float:
    """Compute the normalized mean pairwise Kendall tau distance across a list of string permutations."""
    M: int = len(perms)
    N: int = len(perms[0])
    total: int = 0
    for i, j in combinations(range(M), 2):
        total += kendall_tau_distance(perms[i], perms[j])
    mean_distance: float = (2 * total) / (M * (M - 1))
    normalized: float = mean_distance / (N * (N - 1) / 2)
    return normalized

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

    lock = mp.Lock()
    
    # Create a pool of processes
    with mp.Pool(initializer=init, initargs=(lock,)) as pool:
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
        lists = set()
        actual_lists = []
        head = None
        for i in range(len(items)):
            import ast
            try:
                this_item = ast.literal_eval(items[i])
                actual_lists.append(this_item)
                lists.add(tuple(this_item))
            except SyntaxError:
                pass

        reduced_lists = list(map(lambda x: list(x), lists))
        inversions = count_all_list_pair_inversions(actual_lists)
        kendall_dist = mean_pairwise_kendall_tau(actual_lists)

        import ast
        from collections import Counter
        parsed = [tuple(ast.literal_eval(s)) for s in items if s.strip()]
        counts = Counter(parsed)

        #fractions = [Decimal(count) / Decimal(sum(counts.values())) for count in counts.values()]
        #getcontext().prec = 50
        #e_nondup = expected_trials_to_non_duplicate(fractions)
        #print(f"Expected draws to first non-duplicate ≈ {e_nondup}")

        print(f"N={n}, trials={trials}")
        print(f"Mean Kendall distance: {kendall_dist:1.3f} (ideal near 0.5)")
        print(f"actual inversions: {inversions}")
        print(f"expected inversions: {theoretical_expected_inversions(trials, n)}")
        print(f"ratio (actual over expected inversions): {(100 * inversions / theoretical_expected_inversions(trials, n)):3.0f}%")
        
        print(f"Number of unique orderings: {len(set(items))} out of {len(items)}")
        print(f"Percentage of duplicate orderings: {100 - (len(set(items)) * 100 / len(items)):3.0f}%")
        print(f"  (expected if random: {100*(trials-expected_unique_shuffles(n, trials))/trials:3.0f}%)")
        print(f"Shannon entropy (number of bits): {shannon_entropy(items):3.3f}")

if __name__ == '__main__':
    main()

