import hashlib
import json
class A:
    def __init__(self, v):
        self.v = v
       
    def __repr__(self):
        return f"{self.v}"

orig_list = [A(i % 10) for i in range(100)]
x = list(set(orig_list))
# print(x[0:10])

# Convert entire list to SHA256 and print decimal value of first character

x_json = json.dumps(x, default=lambda o: o.__dict__).encode('utf-8')
ch = hashlib.sha256(x_json).hexdigest()[0]
value = int(ch, base=16)
print(value)
