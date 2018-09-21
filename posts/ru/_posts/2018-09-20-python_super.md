---
layout: post
lang: ru
ref: python_super
title: "Python super() - нюансы кооперативного множественного наследования"
comments: true
tags: [Python]
---

![](/images/diamond_uml.png){:style="float: right;margin-right: 7px;margin-top: 7px;"}
![](/images/object_diamond_uml.png){:style="float: right;margin-right: 7px;margin-top: 7px;"}

## Проблема ромбов при множественном наследовании
Если у класса есть несколько родителей, а у родителей есть общий предок, получаем 
ромб в дереве наследования, как видно на диаграмме `Platypus` (утконос).

Утконос это млекопитающее, обладающее также свойствами рептилиии. 
Таким образом, он формально подходит для множественного наследования - к 
млекопитающему надо добавить свойства рептилии.
Чтобы сделать ситуацию веселеее, в качестве 
[mixin](https://ru.wikipedia.org/wiki/Примесь_(программирование))
я использовал не рептилию, а птицу. 

Поскольку в Python 3 классы, для которых явно не указан предок, наследуются от 
`object`, любая ситуация множественного наследования в Python 3 является 
ромбовидной - в конечном итоге все классы-родители унаследованы от `object`, 
как показано на диаграмме для `ObjectWithMixin`.

Строго говоря, и в диаграмме для `Platypus`, класс `Animal` наследуется от `object`,
но я не стал это визуализировать, чтобы не загромождать диаграмму.

В англоязычной документации ромбы при множественном наследовании называют 
[diamond problem](https://en.wikipedia.org/wiki/Multiple_inheritance#The_diamond_problem).

## Алгоритм C3 поиска в дереве наследования классов Python 3 (MRO)

Для поиска методов и полей в дереве родителей (MRO), Python использует 
[C3 алгоритм](https://ru.wikipedia.org/wiki/C3-линеаризация).

MRO расшифровывается как method resolution order - не слишком удачное название, 
учитывая, что так ищутся не только методы, но и поля.

Совсем упрощенно C3 алгоритм MRO можно представить так:

* в список добавляются родители объекта

  * в конец списка добавляет список родителей этих родителей
  * и так далее
  
* если какой-то класс оказывается в списке дважды, то оставляется только
последнее его вхождение.

Как результат, мы движемся по слоям, не обращаемся к классу-предку до 
того, как обратимся ко всем его потомкам, даже если его потомков у этого
предка несколько.

Например, для класса `Platypus`, метод `draw()` вначале будет искать
в классах `Mammal` и `Bird`, и, только если не найдет там, в `Animal`.

Алгоритм обеспечивает поиск переопределенного метода класса-предка, если
этот метод переопределен хотя бы в одном потомке этого класса-предка.  

Python 2 использовал другой алгоритм (deep first) - если бы он не нашел метод в 
`Mammal`, далее стал бы его искать выше по иерархии, в `Animal`, а не в 
следующем по списку множественного наследования предке, `Bird`. 

С алгоритмом deep first, использовать множественное наследование в Python 3
практически было бы невозможно, поскольку, как сказано выше, любое множественное
наследование в Python 3 является ромбовидным. Мы бы уже через первого родителя 
"проваливались" до `object` и использовали бы реализованые в нем методы, даже 
если они переопределены в других родителях. 

## super()

Функция super() обеспечивает так называемое "кооперативное" наследование методов.
Если во всех объектах использовать эту функцию, то она обеспечит вызов
всех методов из дерева наследования по описанному выше MRO.

Тем кто пришел в Python из Java важно понимать, что `super()` это не класс-родитель,
это прокси с довольно хитрой логикой.

![](/images/animal_class_tree_uml.png){:style="float: right;margin-right: 7px;margin-top: 7px;"}

## Иллюстрация кооперативного множественного наследования с помощью super()


{% highlight python %}
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
            super().draw()
    
    
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
    
        def draw(self):
            super().draw()
    
    
    duckbill = Platypus()
    duckbill.draw()
{% endhighlight %}

    Platypus.__init__()
    Mammal.__init__()
    Bird.__init__()
    Animal.__init__()
    Draw hair
    Draw beak
    Draw body and tail


Но если хоть один наследник нарушает принципы кооперативного наследования (не
вызывает `super()`), то метод родителя вообще не будет вызван, хотя
вроде бы мы имеем явный вызов этого родителя из другого наследника:

{% highlight python %}
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
    
        def draw(self):
            super().draw()
    
    
    duckbill = Platypus()
    duckbill.draw()
{% endhighlight %}

    Platypus.__init__()
    Mammal.__init__()
    Bird.__init__()
    Animal.__init__()
    Draw hair
    Draw beak
    
    
Мы убрали `super()` в `Bird`, и в результате нет вызова
`Animal.draw()` из `Mammal`, хотя там указано `super().draw()`.

Так происходит потому, что `super()` это прокси объект, позволяющий
коллективно(!) обойти список MRO, а вовсе не ссылка на предка. 
И это сработает только если все объекты используют `super()`.
Название скорее вводит в заблуждение.

Код ниже иллюстрирует это. Я добавил аргументы, чтобы вызвать ошибку и явно 
показать что,  например, из `Mammal.__init__` вызывается следующий родитель 
`Platypus`, а вовсе не родитель `Mammal`.

{% highlight python linenos %}
    class Animal:
        def __init__(self):
            print('Animal.__init__()')
    
        def draw(self):
            print('Draw body and tail')
    
    
    class Bird(Animal):
        def __init__(self, beak_length):
            print('Bird.__init__()')
            super().__init__()
    
        def draw(self):
            print('Draw beak')
            #super().draw()
    
    
    class Mammal(Animal):
        def __init__(self, hair_length):
            print('Mammal.__init__()')
            super().__init__()
    
        def draw(self):
            print('Draw hair')
            super().draw()
    
    
    class Platypus(Mammal, Bird):
        def __init__(self):
            print('Platypus.__init__()')
            super().__init__(1)
    
    
    duckbill = Platypus()
{% endhighlight %}
    
    ...
    File "animal_class_tree_arguments.py", line 22, in __init__
        super().__init__()
    TypeError: __init__() missing 1 required positional argument: 'beak_length'

#### Примечание - особенности работы super()

Одним из ограничений `super()` является то, что не получится выполнить операции
([binary operations](https://docs.python.org/3/reference/expressions.html#binary-arithmetic-operations),
[subscriptions](https://docs.python.org/3/reference/expressions.html?highlight=slice#subscriptions)
и т.д.)
над ним, даже если эти операции реализованы в родителе с помощью 
["магических методов"](https://docs.python.org/3/library/operator.html). 

Если выполнить операцию над экземпляром класса, то Python найдет
нужный для выполнения операции "магический метод" в родителе (в примере ниже -
`__getitem__` для индексирования с помощью оператора `[]`).

Но если попытаться выполнить операцию над прокси, возвращаемым `super()`, 
получим ошибку:

{% highlight python %}
    class Parent:
        def __getitem__(self, idx):
            return 0
    
    
    class Child(Parent):
        def index_super(self, idx):
            return super()[idx]
    
    
    kid = Child()
    print(f'Index child: {kid[0]}')
    print(f'Index super: {kid.index_super(0)}')
{% endhighlight %}

    Index child: 0
    ...
    TypeError: 'super' object is not subscriptable
    
