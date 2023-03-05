from typing import List


class Animal:
    escaped: bool


class Bird(Animal):
    pass


class AnimalList(List[Animal]):
    def escaped(self):
        return [mammal for mammal in self if mammal.escaped]


a = AnimalList()
a.append(Bird())  # ok


class Zoo:
    aviary: AnimalList[Bird]  # Mypy: "AnimalList" expects no type arguments, but 1 given [type-arg]
