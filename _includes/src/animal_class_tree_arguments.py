class Animal:
    def __init__(self):
        print('Animal.__init__()')

class Bird(Animal):
    def __init__(self, beak_length):
        print('Bird.__init__()')
        super().__init__()

class Mammal(Animal):
    def __init__(self, hair_length):
        print('Mammal.__init__()')
        super().__init__()

class Platypus(Mammal, Bird):
    def __init__(self):
        print('Platypus.__init__()')
        super().__init__(1)

duckbill = Platypus()
