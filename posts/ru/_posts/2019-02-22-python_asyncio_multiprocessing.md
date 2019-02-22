---
layout: post
lang: ru
ref: python_asyncio_multiprocessing
title: "Как использовать asyncio и multiprocessing в Python"
comments: true
tags: [Python asyncio multiprocessing]
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
    >>>>>>>>>> 0
    >>>>>>>>>> 1
    >>>>>>>>>> 2
    >>>>>>>>>> 3
    <<<<<<<<<< task 2 finished with status 0
    Stdout: b'', Stderr: b''
    >>>>>>>>>> 4
    <<<<<<<<<< task 1 finished with status 0
    Stdout: b'', Stderr: b''
    >>>>>>>>>> 5
    <<<<<<<<<< task 3 finished with status 0
    Stdout: b'', Stderr: b''

Этот код запускает максимум три экземпляра внешнего процесса.
Я ограничиваю это с помощью [asyncio.Queue](https://docs.python.org/3/library/asyncio-queue.html).

Когда процесс завершается вы можете обработать его результаты.
Следующий процесс запустится автоматически так что в любой момент времени
будет работать одновременно максимум процесса.

Как видите, код очень прост и содержит практически только прикладную логику.

Он выглядит как синхронный.
То есть как предположительный старый код, который запускал только один 
процесс и который мы теперь конвертировали в асинхронный.
