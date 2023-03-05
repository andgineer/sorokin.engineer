---
layout: post
lang: ru
ref: python_type_aliasing
title: "Псевдонимы типов и генерики в Python"
comments: true
tags: [Python, mypy, class]
---

![](/images/safari.jpeg){:.post-title}

### Как исправить загадочную ошибку Python `Mypy: expects no type arguments, but 1 given [type-arg]`

Приходилось ли вам слышать про псевдонимы типов в Питоне? 

На первый взгляд, [теория](https://mypy.readthedocs.io/en/stable/generics.html#generic-type-aliases)
выглядит сложной и абстрактной. Давайте разберемся на элементарном примере.

Представьте, что у вас список животных. 
И у вас есть функция `escaped()` применимая к списку любых животных.

Но по каким-то причинам вам нужны специализированные списки - список птиц, список рептилий и т.д. 

И вам хочется использовать проверки типов, чтобы нельзя было добавить птицу в список рептилий.

_Я в курсе про летающих динозавров, но давайте без педантизма, тем более что летающие динозавры - не птицы._


Пишем простейших код.. и ловим совсем невнятную ошибку:

{% highlight python %}
{% include src/type_aliasing_initial.py %}
{% endhighlight %}

Что это за `[type-arg]` и почему нет проблем с `List[Bird]` но нельзя `AnimalList[Bird]`?

`List[Animal]` создает список для конкретного класса, в отличие от исходного генерика `list`.

И уже просто негде указывать тип элементов для `AnimalList` - это уже не генерик.

Решение элементарно - надо создать alias для типа `Animal`. 
Тогда в `AnimalList` останется возможность указать тип элементов.

{% highlight python %}
{% include src/type_aliasing.py %}
{% endhighlight %}

Если вам это кажется абстрактным вопросом без практического применения, посмотрите на [мой код](https://github.com/andgineer/goodreads-export/blob/7b19c1f500e26e5d70dcbfd709f130f83be212f5/src/goodreads_export/templates.py#L150)
использующий type alias точно для такой ситуации.

Если вам интересно, что за аргумент `bound` в `TypeVar` в коде выше, то это просто заставляет определяемый type alias принимать как `Animal` 
так и любого наследника `Animal`.
