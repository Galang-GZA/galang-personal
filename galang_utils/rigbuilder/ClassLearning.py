class Cake:
    def __init__(self, flavor):
        self.flavor = flavor

    def describe(self):
        print(f"This cake is {self.flavor}-flavored!")


cake1 = Cake("chocolate")
cake1.describe()
