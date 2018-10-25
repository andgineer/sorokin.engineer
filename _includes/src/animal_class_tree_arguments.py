class Vertebrate:
    def __init__(self):
        print('Vertebrate.__init__()')

class Bird(Vertebrate):
    def __init__(self, beak_length):
        print('Bird.__init__()')
        super().__init__()

class Mammal(Vertebrate):
    def __init__(self, hair_length):
        print('Mammal.__init__()')
        super().__init__()

class Platypus(Mammal, Bird):
    def __init__(self):
        print('Platypus.__init__()')
        super().__init__(1)

duckbill = Platypus()
