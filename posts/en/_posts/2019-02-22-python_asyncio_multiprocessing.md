---
layout: post
lang: en
ref: python_asyncio_multiprocessing
title: "How to use asyncio with multiprocessing in Python"
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

Python [multiprocessing module](/posts/en/python_async.html) gives you great tools to write applications with
clear logic.

But sometimes you want to convert old code that use external process. 
So now it will lunch many instances of the external process 
simultaneously. 

You can rewrite it completely to use multiprocessing module.

Or you can use `asyncio` and leave old code intact. This way you don't have to
spend a lot of time in debugging new application logic.

I'll show you how.

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

This code starts maximum three instances of external process.
I limited that with help of [asyncio.Queue](https://docs.python.org/3/library/asyncio-queue.html).

When external process is finished your code can process the result.
And next process will be start automatically so at any moment
there would be at max three processes running.

As you can see the code is pretty straightforward and looks like
synchronous code that supposedly you are converting.

So you just care about your application logic and do not over-complicate it
with multiprocessing boilerplates.
