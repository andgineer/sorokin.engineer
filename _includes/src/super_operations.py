class Parent:
    def __getitem__(self, idx):
        return 0

class Child(Parent):
    def index_super(self, idx):
        return super()[idx]

kid = Child()
print(f'kid[0]: {kid[0]}')
print(f'kid.index_super(0): {kid.index_super(0)}')