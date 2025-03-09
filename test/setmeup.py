class A:
    def __init__(self, v):
        self.v = v
       
    def __repr__(self):
        return f"{self.v}"

orig_list = [A(i % 10) for i in range(1_000)]
x = list(set(orig_list))
print(x[0])
