class Vertebrate:
    def lay_eggs(self):
        return None

class Bird(Vertebrate):
    def lay_eggs(self):
        return True

class Mammal(Vertebrate):
    pass

class PlatypusMammalFirst(Mammal, Bird):
    pass

class PlatypusBirdFirst(Bird, Mammal):
    pass

print(PlatypusMammalFirst().lay_eggs())
print(PlatypusBirdFirst().lay_eggs())
