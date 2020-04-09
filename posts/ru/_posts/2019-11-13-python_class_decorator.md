---
layout: post
lang: ru
ref: python_class_decorator
title: "Декоратор-класс работающий и для отдельных функций и для методов объектов Python"
comments: true
tags: [python, class, decorator]
---
![](/images/decorators.png){:.post-title}

Основы использования декораторов Python описаны в интернете в тысячах постов на сотнях языков,
поэтому я не буду тут повторно описывать основы.

После того, как вы поняли основы, вас может ввести в тупик казалось бы простая задача.
Мы хотим написать декоратор в виде класса, и применить этот декоратор к методу класса.

Скажем, мы хотим добавить декторатор к методу `func_to_wrap`:

{% highlight python %}
class ClassToWrap:
    def func_to_wrap(self):
        self.name += '!'
        print(self.name)
        return self.name
{% endhighlight %}

Пишем по учебнику класс-декторатор:

{% highlight python %}
class Decorator:
    def __init__(self, orig_func):
        self.orig_func = orig_func

    def __call__(self, *args):
        return self.orig_func(*args)
{% endhighlight %}

Пытаемся применить его к методу `func_to_wrap` и получаем ошибку 
{% highlight python %}
class ClassToWrap:
    @Decorator
    def func_to_wrap(self):
        self.name += '!'
        print(self.name)
        return self.name
        
c = ClassToWrap()
c.func_to_wrap()
{% endhighlight %}
    func_to_wrap() missing 1 required positional argument: 'self'

Секрет в том что `Decorator.__call__` вызывает `func_to_wrap` не передавая ей `self` - тот `self` что
получил `Decorator.__call__` это его собственный экземляр (объект класса `Decorator`), а экземляр 
`ClassToWrap` вообще нигде не передается. Основная причина в том что `orig_func` это `unbound`,
не привязанный к экземпляру объекта, а требующий указания экземпляра в первом аргументе.

На этом можно было бы и закончить - так устроены дектораторы-классы. Если вам нужен декоратор метода
объекта, то используйте декораторы-функции, там все будет работать ожидаемо - первый аргумент будет `self`
декорируемого объекта `ClassToWrap`.

Но решить задачу можно и с помощью декоратора-класса. Более того, можно даже сделать универсальное решение,
которое можно использовать и как декторатор отдельных функций, и как декоратор методов объектов.

Для этого мы можем задействовать механизм дескрипторов. Напомню, что если атрибут объекта имеет метод `__get__` 
то при обращении к нему Python вернет не сам этот объект, а то что возвращает метод `__get__`.

Ниже приведен работающий код.

В нем метод `UniversalDecorator.__call__` будет вызываться при декорировании функций.
Если же вы декорируете метод объекта, то Python не будет его вызывать - он вызовет `__get__` и в ответ получит
экземпляр `WrapperHelper` в который мы уже закинули ссылки как на экземляр `ClassToWrap` так и на `Decorator`.

Далее Python вызовет результат `__get__` как функцию, а поскольку это объект с методом
`__call__` (`class WrapperHelper`) он вызовет метод
`WrapperHelper.__call__`. 

Он вызывает объект-декоратор, что означает вызов его `__call__`. В этот вызов `WrapperHelper.__call__` 
подставит экземпляр декорируемого класса `ClassToWrap`, который попадет как первый элемент в `*args` (строка
6). И у нас произойдет корректный вызов декорированного метода `func_to_wrap` - первым ее аргументом будет
экземпляр класса `ClassToWrap`. 

<script src="https://gist.github.com/andgineer/026a617528c5740da24ec984ac282ee6.js"></script>
