---
layout: post
lang: ru
ref: 2021-08-02-async_nullcontext
title: "Асинхронный вариант (asincio) пустого менеджера контекста (nullcontext) в Python"
comments: true
tags: [python asyncio]
---

![](/images/context.jpeg){:.post-title}

Если вы используете [менеджер контекста](https://realpython.com/python-with-statement/) 
в операторе `with` и вам нужно сделать его использование опциональным, то можно применить
[nullcontext](https://docs.python.org/3/library/contextlib.html#contextlib.nullcontext) 
как вариант "не использовать менеджер контекста"".

Например в функцию передается `s3` boto client но функция может создать и свой, если он не передан:

<script src="https://gist.github.com/andgineer/1777396a8ed299fdd43e9d6c1869e01e.js"></script>

Но, например, в [aiobotocore](https://aiobotocore.readthedocs.io/en/latest/) вам нужен асинхронный
менеджер контекста:

<script src="https://gist.github.com/andgineer/8602627b3e6e95f0e189a59f96b37c4b.js"></script>

В Python нет асинхронного варианта для nullcontext.

Как решение вы можете использовать [AsyncExitStack](https://docs.python.org/3/library/contextlib.html#contextlib.AsyncExitStack):

<script src="https://gist.github.com/andgineer/0908a17259fd89a9ef568d475821dece.js"></script>
