from typing import List, TypeVar


class Animal:
    escaped: bool


AnimalSubClass = TypeVar("AnimalSubClass", bound=Animal)


class Bird(Animal):
    pass


class Reptile(Animal):
    pass


class AnimalList(List[AnimalSubClass]):
    def escaped(self):
        return [mammal for mammal in self if mammal.escaped]


class Zoo:
    aviary: AnimalList[Bird]


aviary = Zoo()
aviary.aviary.append(Bird())  # ok
aviary.aviary.append(Reptile())  # Mypy: Argument 1 to "append" of "list" has incompatible type "Reptile"; expected "Bird" [arg-type]
