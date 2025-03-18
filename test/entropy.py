import math
from collections import Counter

N = 20 # length of each sequence
TRIALS = 1024 # number of trials

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

tuples = []

for i in range(TRIALS):
    objs = [MyObj(f"obj_{i}") for i in range(N)]
    obj_set = set(objs)

    l = list(o.name for o in obj_set)
    # l.sort(key=lambda a: id(a))
    tuples.append(hash(tuple(l)))

print(f"Percentage of duplicate orderings: {100 - (len(set(tuples)) * 100 / TRIALS)}%")
print(f"Shannon entropy (number of bits): {shannon_entropy(tuples)}")
