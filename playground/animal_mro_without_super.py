class Animal:
    def draw(self):
        print('Draw body and tail')


class Bird(Animal):
    def draw(self):
        print('Draw beak')


class Mammal(Animal):
    pass


class Platypus(Mammal, Bird):
    pass


duckbill = Platypus()
duckbill.draw()