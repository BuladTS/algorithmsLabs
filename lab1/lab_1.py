from my_array import array as ar
import array
a = ar("d", [1, 2, 4, 3, 4])
b = [1, 2, 4, 3, 4]


print(a.__eq__(b))
print("-" * 50)
for i in a:
    print(i)
print("-" * 50)
