class Animal:
    def __init__(self):
        print('Animal.__init__()')

    def draw(self):
        print('Draw body and tail')


class Bird(Animal):
    def __init__(self):
        print('Bird.__init__()')
        super().__init__()

    def draw(self):
        print('Draw beak')
        #super().draw()


class Mammal(Animal):
    def __init__(self):
        print('Mammal.__init__()')
        super().__init__()

    def draw(self):
        print('Draw hair')
        super().draw()


class Platypus(Mammal, Bird):
    def __init__(self):
        print('Platypus.__init__()')
        super().__init__()



duckbill = Platypus()
duckbill.draw()