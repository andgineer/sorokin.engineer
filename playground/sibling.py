class Employee:
    def __init__(self, name, salary):
        pass

class Checf2(Employee):
    def __init__(self, name):
        super().__init__(name, 50000)

class Server2(Employee):
    def __init__(self, name):
        super().__init__(name, 50000)

class Two(Checf2, Server2):
    pass

tom = Two('Tom')