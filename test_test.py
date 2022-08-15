class A:
    def __init__(self, data):
        self.data = data

    def stuff(self):
        self.data.check_data()


class B(A):
    def stuff_b(self):
        print(f'data is {self.data}')


class MyData:
    def check_data(self):
        print('data is ok')


# d = None
# d = MyData()
# print(d)
# b = B(d)
# b.data = MyData(
# b.stuff_b()
# d = MyData()
# print(d)
# b.stuff_b()
a = MyData()
print(f"a is {a}")
b = a
print(f"b is {b}")
print("change a")
a = MyData()
print(f"a is {a}")
print(f"b is {b}")
