---
layout: post
lang: en
ref: 2021-08-02-async_nullcontext
title: "Python asyncio version of nullcontext"
comments: true
tags: [python asyncio]
---

![](/images/context.jpeg){:.post-title}

If you are using [context manager](https://realpython.com/python-with-statement/) optionally in `with` 
statement, you use   
[nullcontext](https://docs.python.org/3/library/contextlib.html#contextlib.nullcontext) 
as option to not use context manager.

For example if you have function that can use external `s3` boto client but create it if it's not provided:

<script src="https://gist.github.com/andgineer/1777396a8ed299fdd43e9d6c1869e01e.js"></script>

But what if context you are using is async one, like with [aiobotocore](https://aiobotocore.readthedocs.io/en/latest/):

<script src="https://gist.github.com/andgineer/8602627b3e6e95f0e189a59f96b37c4b.js"></script>

There is no asyncio counterpart for nullcontext in Python.

But you can use [AsyncExitStack](https://docs.python.org/3/library/contextlib.html#contextlib.AsyncExitStack):

<script src="https://gist.github.com/andgineer/0908a17259fd89a9ef568d475821dece.js"></script>
