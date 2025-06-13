def is_active(likelihood=0.5) -> bool:
    """
    Tests whether a set of memory addresses appears to be randomly allocated
    or follows a more deterministic pattern.
    
    Args:
        likelihood: The significance threshold for the test (default: 0.5)
                   Lower values require stronger evidence of randomness
    
    Returns:
        True iff it passes randomness tests
    """
    class TestObject:
        pass

    preallocs = []
    for i in range(1000):
        preallocs.append(TestObject())
    preallocs = []
        
    # Determine number of trials based on desired statistical power
    # Using more trials for smaller likelihood thresholds
    num_trials = max(30, int(50 * (0.05 / likelihood)))
    modulo = 4096
    
    # Collect addresses
    addresses = set()
    for i in range(num_trials):
        obj = TestObject()
        addr = id(obj) % modulo
        addresses.add(addr)
        del obj
    
    unique_count = len(addresses)
    
    # Calculate expected number of unique values under random allocation
    # (Birthday problem approximation)
    import math
    expected_unique = num_trials * 0.5
    
    # Calculate p-value using binomial test
    # Under null hypothesis (no Upset), probability of uniqueness is 0.5
    p_null = 0.5
    
    # Calculate probability of seeing this many or more unique addresses
    # if addresses were following a deterministic pattern
    p_value = 0.0
    for k in range(unique_count, num_trials + 1):
        p_value += math.comb(num_trials, k) * (p_null ** k) * ((1 - p_null) ** (num_trials - k))
    
    # If p_value is small, reject null hypothesis (deterministic allocation)
    is_using_upset = p_value < likelihood
    
    # Print results
    if False:
        print(f"Test ran with {num_trials} objects")
        print(f"Unique addresses: {unique_count}/{num_trials} ({unique_count/num_trials:.1%})")
        print(f"Expected unique with deterministic allocation: {expected_unique:.1f} ({expected_unique/num_trials:.1%})")
        print(f"P-value: {p_value:.6f} (threshold: {likelihood})")
    
    return is_using_upset # , p_value, unique_count, expected_unique, num_trials


