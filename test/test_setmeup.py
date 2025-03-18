class MyObj:
    def __init__(self, name):
        self.name = name
    def __repr__(self):
        return self.name
    # No __hash__ override, so the default identity-based hashing is used.

def demonstrate_address_randomization(n):
    """
    Create custom objects that rely on Python's default identity-based hash.
    That default is tied to the object's memory address, which can change
    from run to run when ASLR is enabled.
    
    By putting these objects into a set and printing their names in iteration
    order, we can see the effect of differing addresses (i.e., the set iteration
    order may vary). This demonstrates address randomization without calling
    id(), repr(), or hash() directly.
    """
    objs = [MyObj(f"object_{i}") for i in range(n)]
    obj_set = set(objs)
    # The iteration order of these MyObj instances can differ from run to run
    # because their identity hashes (memory addresses) may change.
    # print("Set iteration order for custom objects (address-based hashing):")
    r = [o.name for o in obj_set]
    return r

def hashme(x):
    # Convert entire list to SHA256 and print decimal value of first character
    import hashlib
    import json
    x_json = json.dumps(x, default=lambda o: o.__dict__).encode('utf-8')
    digest = hashlib.sha256(x_json).hexdigest()
    return digest
    #ch = digest[0]
    #value = int(ch, base=16)
    #return value

    
def test_setmeup():
    order_hist = set()
    num_lists = 1000
    length = 30
    for i in range(num_lists):
        x = demonstrate_address_randomization(length)
        order_hist.add(hashme(x))
    # Below is almost certainly true with `upset`, and almost certainly false without.
    # A small number for len(order_hist) corresponds to a low level of randomization
    assert len(order_hist) == num_lists

if __name__ == "__main__":
    # print(hex(id("hello")))
    test_setmeup()
