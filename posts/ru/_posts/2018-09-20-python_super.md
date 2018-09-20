---
layout: post
lang: ru
ref: python_super
title: "Python super() - нюансы кооперативного вызова унаследованных методом"
comments: true
tags: [Python]
---

![](/images/diamond_uml.png){:style="float: right;margin-right: 7px;margin-top: 7px;"}
![](/images/object_diamond_uml.png){:style="float: right;margin-right: 7px;margin-top: 7px;"}

## Ромбовидное наследование - C3 MRO
Ромбовидное наследование (в англоязычной документации - diamond) это когда
у класса есть несколько родителей (т.е. это 
[mixin](https://ru.wikipedia.org/wiki/Примесь_(программирование)) 
в классической терминологии), а у родителей есть общий предок.

Поскольку в Python 3 все классы наследуются в конечном итоге от `object`, формально
любая ситуация множественного наследования является ромбовидной (поскольку в конечном
итоге все классы-родители унаследованы от `object`):

Для поиска методов и полей в дереве родителей, Python использует так называемый C3 алгоритм 
MRO (method resolution order - не слишком удачное название, учитывая, что так ищутся 
не только методы).

Совсем упрощенно алгоритм можно представить так 

* составляется список родителей объекта

  * рекурсивно добавлет к нему списки родителей этих родителей и так далее.
  
* если какой-то класс оказывается в этом списке дважды, то оставляется только
последнее его вхождение.

По смыслу - мы движемся по слоям, не обращаемся к слишком далекому предку до того,
как обратимся ко всем его потомкам, даже если его потомков несколько.


## super()

Функция super() обеспечивает так называемое "кооперативное" наследование методов.
Если во всех объектах дерева использовать эту функцию, то она обеспечит вызов
всех унаследованных методов по описанному выше MRO.

Тем кто пришел в Python из Java важно понимать, что `super()` это не родитель,
это прокси с довольно хитрой логикой.

Одним из ограничей `super()` является то, что не получится выполнить операции
над ним, даже если эти операции реализованы с помощью "магических методов"
в родителе. 

Если выполнить операцию над экземпляром наследника, то Python найдет
нужный для выполнения операции "магический метод" в родителе.
Но если попытаться выполнить операцию над прокси, возвращаемым `super()`, получим ошибку:

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
            print('Draw nose')
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
    Draw nose
    Draw beak
    Draw body and tail


Но если хоть один наследник нарушает принципы кооперативного наследования (не
вызывает `super()`) то метод родителя вообще не будет вызван, хотя
вроде бы мы имеем явный вызов в классе `Mammal`:

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
            print('Draw nose')
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
    Draw nose
    Draw beak
    
    
Мы не вызываем `super()` в `Bird` а в результате нет вроде бы явного вызова
из `Mammal`.

Так происходит потому, что `super()` это прокси объект, реализующий
MRO, а вовсе не ссылка на предка, т.е. название скорее вводит в заблуждение.

Python для показанной выше иерархии объектов строит MRO, в котором убран 
повтор `Animal` для первого из предков (`Mammal`).
 
А, поскольку второй предок, `Bird` теперь не вызывает  метод `draw()`
из MRO (с помощью `super()`), `Animal.draw()` не вызывается вовсе.
