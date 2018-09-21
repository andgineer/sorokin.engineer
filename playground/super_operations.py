class Parent:
    def __getitem__(self, idx):
        return 0


class Child(Parent):
    def index_super(self, idx):
        return super()[idx]


kid = Child()
print(f'Index child: {kid[0]}')
print(f'Index super: {kid.index_super(0)}')