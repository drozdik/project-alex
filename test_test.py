ddict = {"a": 0}
ddict["a"] = 3

class B:
    def __init__(self, my_d):
        self.my_d = my_d

    def print_me(self):
        print(self.my_d["a"])


b = B(ddict)
b.print_me()
ddict["a"] = 5
b.print_me()