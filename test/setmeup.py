def demonstrate_address_randomization():
    """
    Create custom objects that rely on Python's default identity-based hash.
    That default is tied to the object's memory address, which can change
    from run to run when ASLR is enabled.
    
    By putting these objects into a set and printing their names in iteration
    order, we can see the effect of differing addresses (i.e., the set iteration
    order may vary). This demonstrates address randomization without calling
    id(), repr(), or hash() directly.
    """
    class MyObj:
        def __init__(self, name):
            self.name = name
        # No __hash__ override, so the default identity-based hashing is used.

    objs = [MyObj(f"obj_{i}") for i in range(5)]
    obj_set = set(objs)
    # The iteration order of these MyObj instances can differ from run to run
    # because their identity hashes (memory addresses) may change.
    print("Set iteration order for custom objects (address-based hashing):")
    print([o.name for o in obj_set])

demonstrate_address_randomization()


class A:
    def __init__(self, v):
        pass
        # self.v = f"A is object {v*1000}" * ((v % 3) + 1)
       
    #def __repr__(self):
    #    return self.v

orig_list = [f"{i % 10}" for i in range(1000)]
# print(orig_list[0], orig_list[1])
x = list(set(orig_list))
print(x[0])
# print(x)
# print(x[0:10])

#print(x[0])

if False:
    # Convert entire list to SHA256 and print decimal value of first character
    import hashlib
    import json
    x_json = json.dumps(x, default=lambda o: o.__dict__).encode('utf-8')
    ch = hashlib.sha256(x_json).hexdigest()[0]
    value = int(ch, base=16)
    print(value)
