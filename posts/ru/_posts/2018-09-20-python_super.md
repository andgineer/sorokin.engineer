---
layout: post
lang: ru
ref: python_super
title: "Python super() - нюансы кооперативного наследования"
comments: true
tags: [Python]
---

![](/images/diamond_uml.png){:style="float: right;margin-right: 7px;margin-top: 7px;"}
![](/images/object_diamond_uml.png){:style="float: right;margin-right: 7px;margin-top: 7px;"}

## Ромбовидное наследование
Ромбовидное наследование (в англоязычной документации - diamond) это ромбы в дереве
наследования.

Если у класса есть несколько родителей, а у родителей есть общий предок, получаем 
ромб в дереве наследования, как видно на диаграмме `Platypus` (утконос).
Утконос это и птица и млекопитающее, каждый из которых, в свою очередь, является
животным.

Поскольку в Python 3 классы, для которых явно не указан предок, наследуются от 
`object`, любая ситуация множественного наследования является ромбовидной -
поскольку в конечном итоге все классы-родители унаследованы от `object`, как
показано на диаграмме для `ObjectWithMixin`.

Строго говоря, и в диаграмме для `Platypus`, класс `Animal` наследуется от `object`,
но я не стал это визуализировать, чтобы не загромождать диаграмму.

## Алгоритм C3 поиска (MRO) в дереве наследования классов Python

Для поиска методов и полей в дереве родителей, Python использует так называемый C3 
алгоритм MRO.

MRO расшифровывается как method resolution order - не слишком удачное название, 
учитывая, что так ищутся не только методы, но и поля.

Совсем упрощенно алгоритм можно представить так:

* составляется список родителей объекта

  * рекурсивно добавляет к нему списки родителей этих родителей и так далее.
  
* если какой-то класс оказывается в списке дважды, то оставляется только
последнее его вхождение.

Как результат, мы движемся по слоям, не обращаемся к слишком далекому предку до 
того, как обратимся ко всем его потомкам, даже если его потомков несколько.


## super()

Функция super() обеспечивает так называемое "кооперативное" наследование методов.
Если во всех объектах использовать эту функцию, то она обеспечит вызов
всех методов из дерева наследования по описанному выше MRO.

Тем кто пришел в Python из Java важно понимать, что `super()` это не класс-родитель,
это прокси с довольно хитрой логикой.

#### Примечание - особенности работы super()

Одним из ограничений `super()` является то, что не получится выполнить операции
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

![](/images/animal_class_tree_uml.png){:style="float: right;margin-right: 7px;margin-top: 7px;"}

## Иллюстрация кооперативного наследования с помощью super()


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
    
    
Мы не вызываем `super()` в `Bird`, а в результате нет вроде бы явного вызова
`Animal` из `Mammal`.

Так происходит потому, что `super()` это прокси объект, реализующий
MRO, а вовсе не ссылка на предка. Название скорее вводит в заблуждение.

Python для показанной выше иерархии объектов строит список для MRO, в котором 
убрано первое появление `Animal` (для `Mammal`), а оставлено только
последнее (для `Bird`).
 
Поскольку в `Bird` в этом варианте кода не вызывается `super().draw()`, 
то `Animal.draw()` не вызывается вовсе.
