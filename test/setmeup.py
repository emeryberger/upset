class A:
    def __init__(self, v):
        self.v = v
       
    def __repr__(self):
        return f"0000000000000{self.v}"

orig_list = [A(i) for i in range(100)]
x = list(set(orig_list))
print(x[0])
