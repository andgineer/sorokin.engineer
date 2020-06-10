---
layout: post
lang: ru
ref: python_import_asterisk
title: "Автоматизация импорта из Python моделей каталога (from * import *)"
comments: true
tags: [python]
---
![](/images/python_import.jpg){:style="float: left;margin-right: 7px;margin-top: 7px;"}

Если вам надоело писать в `__init__.py` для каждого файла пакета

{% highlight python %}
from foo import *
from bar import *
{% endhighlight %}

У меня есть простой код, автоматизирующий это.

Но давайте вначале разберемся, зачем такое писать вовсе?
Во многих случаях это просто плохой стиль, которого я рекомендую вам избегать.
Вы смешиваете в пространстве имен имена из других модулей и потом в этой каше
очень просто наделать труднообнаружимых ошибок.

Но допустим у вас есть проект, где все модели аккуратно разложены в отдельные файлы
(например потому что их много, а также чтобы изменение в
разных моделях не изменяло один файл, что обычно усложняет git merge)

{% highlight python %}
- model.py
    - user.py
        class User(Base):
            ...
    - order.py
        class Order(Base):
            ...
{% endhighlight %}

Мне далее было бы удобнее писать так

{% highlight python %}
- controllers.py
    - add_user.py
        from model import User, Order
        def add_user(user: User, order: Order):
            ...
{% endhighlight %}

Но придется

{% highlight python %}
- controllers.py
    - create_order.py
        from model.user import User
        from model.order import Order
        def add_user(user: User, order: Order):
            ...
{% endhighlight %}

Кошмар..

Исправить конечно не сложно - добавим `__init__.py`:

{% highlight python %}
- model.py
    - __init__.py
        from .user import *
        from .order import *
    - user.py
        class User(Base):
            ...
    - order.py
        class Order(Base):
            ...
{% endhighlight %}

Но как же занудно потом не забывать добавлять такие `import` строчки для
каждой новой модели.

Стоп! Это же Python - автоматизировать можно абсолютно что угодно!

Код ниже автоматизирует нужный нам `from * import *`.
<script src="https://gist.github.com/andgineer/141f97164aaea12215cf9a2aed332c1d.js"></script>

На строке 8 перебираем файлы пакета используя
[Path.globe()](https://docs.python.org/3/library/pathlib.html#pathlib.Path.glob).

На строке 9 проверяем что это не подкаталог и что имя не начинается с подчеркивания 
(чтобы исключить `__init__.py` и прочие файлы имя которых вы можете начать с 
подчеркивания,
чтобы они не участвовали в этой магии).

Строка 10 импортирует очередной файл как модуль Python используя относительное имя
(видите точку в начале имени?).

Строка 11 получает список всех не служебных имен модуля.

И наконец на строке 12 добавляем все имена из модуля в наш `__init__.py`.
