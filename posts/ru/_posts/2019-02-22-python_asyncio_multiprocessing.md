---
layout: post
lang: ru
ref: python_asyncio_multiprocessing
title: "Как использовать asyncio и multiprocessing в Python"
comments: true
tags: [Python, asyncio, multiprocessing]
redirect_from: "/posts/ru/python_asyncio_multiprocessing/"
---
![](/images/wool-yarn.jpg){:style="float: right;margin-right: 7px;margin-top: 7px;"}

<style type="text/css">
  h2 {
    content: "";
    clear: both;
  }
</style>

Модуль [multiprocessing module](/posts/ru/python_async.html) 
позволяет вам писать компактные приложения использующие множество процессов.

Но иногда у вас есть старый код который запускал один процесс и вы хотите
чтобы теперь он запускал несколько одновременно. 

Вы можете полностью переписать его используя модуль multiprocessing.
 
Но тогда вам придется заново отлаживать это по сути новое приложение.

Я предлагаю иной подход - чуть модифицировать ваш старый код, добавив
в него asyncio. В итоге ваше приложение по сути останется тем же,
вам не потребуется долго отлаживать его заново.

{% highlight python %}
{% include src/asyncio_multiprocessing.py %}
{% endhighlight %} 
    >>>>> task 0 starts with delay 0.9 seconds
    >>>>> task 1 starts with delay 0.4 seconds
    >>>>> task 2 starts with delay 0.6 seconds
    <<<<< task 1 finished with status 0
    Stdout: b'', Stderr: b''
    >>>>> task 3 starts with delay 0.3 seconds
    <<<<< task 3 finished with status 0
    Stdout: b'', Stderr: b''
    <<<<< task 2 finished with status 0
    Stdout: b'', Stderr: b''
    >>>>> task 4 starts with delay 0.9 seconds
    >>>>> task 5 starts with delay 0.3 seconds
    <<<<< task 0 finished with status 0
    Stdout: b'', Stderr: b''
    <<<<< task 5 finished with status 0
    Stdout: b'', Stderr: b''
    <<<<< task 4 finished with status 0
    Stdout: b'', Stderr: b''

Process finished with exit code 0


Этот код запускает 6 задач в максимум трех одновременно работающих экземплярах внешнего процесса.
Я ограничиваю это с помощью [asyncio.Queue](https://docs.python.org/3/library/asyncio-queue.html).

Когда процесс завершается вы можете обработать его результаты.
Следующий процесс запустится автоматически так что в любой момент времени
будет работать одновременно максимум процесса.

Как видите, код очень прост и содержит практически только прикладную логику.

Он выглядит как синхронный.
То есть как предположительный старый код, который запускал только один 
процесс и который мы теперь конвертировали в асинхронный.
