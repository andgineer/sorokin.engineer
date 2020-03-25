---
layout: post
lang: ru
ref: python_asyncio
title: "Асинхронный код Python из синхронного приложения"
comments: true
tags: [python, asyncio]
---
![](/images/wool-yarn.jpg){:style="float: left;margin-right: 7px;margin-top: 7px;"}

Что такое асинхронный код и зачем он вам может понадобиться я рассказывал в статье [Несинхронный Python](https://sorokin.engineer/posts/ru/python_async.html).

Иногда, например при экспериментах в [REPL](https://ru.wikipedia.org/wiki/REPL) 
или отладке у нас возникает необходимость запускать асинхронный код из синхронных приложений Python.

Раньше это было довольно громоздко

{% highlight python %}
{% include src/sync_async_old.py %}
{% endhighlight %}
    Hello World!

С выходом Python 3.7 появился упрощенный способ запуска без явного создания цикла - функция [asyncio.run](https://docs.python.org/3/library/asyncio-task.html#asyncio.run)

{% highlight python %}
{% include src/sync_async_py37.py %}
{% endhighlight %}
    Hello World!

А Python 3.8 позволяет нам сразу запустить REPL в асинхронном режиме (`python -m asyncio`).

Если приведенный выше код в файле sync_async.py то в Python 3.8 можно:

{% highlight bash %}
python -m asyncio
>>> import sync_async
>>> await sync_async.main()
{% endhighlight %}
    Hello World!