import ctypes

class A:
    def __init__(self, v):
        self.v = v
        self.pad = ctypes.create_string_buffer(1)
       
    def __repr__(self):
        return f"A({self.v})"
    

orig_list = [A(i) for i in range(10)]
x = list(set(orig_list))
print(x[0])
