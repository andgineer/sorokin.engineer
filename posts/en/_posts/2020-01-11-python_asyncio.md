---
layout: post
lang: en
ref: python_asyncio
title: "Async Python code from sync code"
comments: true
tags: [python, asyncio]
---
![](/images/wool-yarn.jpg){:style="float: left;margin-right: 7px;margin-top: 7px;"}

About async Python and why do you need it you can find from
article [Non-sequential Python](https://sorokin.engineer/posts/en/python_async.html).

Sometimes you want to call async code from sync evironment like [REPL](https://en.wikipedia.org/wiki/Read%E2%80%93eval%E2%80%93print_loop).

Before Python 3.7 it was not easy

{% highlight python %}
{% include src/sync_async_old.py %}
{% endhighlight %}
    Hello World!

In Python 3.7 we have function [asyncio.run](https://docs.python.org/3/library/asyncio-task.html#asyncio.run)

{% highlight python %}
{% include src/sync_async_py37.py %}
{% endhighlight %}
    Hello World!

And in Python 3.8 we even can run REPL in async mode (`python -m asyncio`).

Suppose the code above is in file sync_async.py:

{% highlight bash %}
python -m asyncio
>>> import sync_async
>>> await sync_async.main()
{% endhighlight %}
    Hello World!