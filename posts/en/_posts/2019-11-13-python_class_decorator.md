---
layout: post
lang: en
ref: python_class_decorator
title: " Python decorator class to decorate standalone functions and object methods"
comments: true
tags: [python, class, decorator]
---
![](/images/decorators.png){:.post-title}

The advanced technique that I describe below assumes you understand basic
mechanic of Python decorators and Python descriptors. 

Suppose we want to decorate method `func_to_wrap` of the class `ClassToWrap`.

If we create Python decorator class as below:

{% highlight python %}
class Decorator:
    def __init__(self, orig_func):
        self.orig_func = orig_func

    def __call__(self, *args):
        return self.orig_func(*args)
{% endhighlight %}

We will fail to use it:

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

As we can see from the error `Decorator.__call__` calls `func_to_wrap` without 
`self`. This is because `orig_func` is `unbound`,
it's not bound to object instance and we have to pass the instance as first argument. 
But we cannot!

The `self` inside `Decorator.__call__` is the instance of `Decorator`. 

We do not have `ClassToWrap` instance inside `Decorator.__call__`.  

Of cause there is simple solution - write the decorator as function.

But I am goin to show you how to write decorator as class, using Python descriptors. 

Moreover the decorator will be universal and
could be applied to standalone functions as well as to object methods.

The Python descriptor protocol is very simple - if object attribute has method `__get__` 
then Python will call it and return as the attribute value the result of `__get__`.

Below you can see working example.

The `UniversalDecorator.__call__` will work if we decorate standalone functions.

For class method instead of `__call__` Python will call `__get__` and after that call the result of it as a function.

`UniversalDecorator.__get__` returns `WrapperHelper` 
with links to both `ClassToWrap` and `Decorator` instances.

When Python call the `__get__` result (instance of `WrapperHelper`) it will actually call
`WrapperHelper.__call__`. 

`WrapperHelper.__call__` add instance of `ClassToWrap`, as first item in `*args` (line
6). So `func_to_wrap` will get instance of `ClassToWrap` as first argument. 

<script src="https://gist.github.com/andgineer/026a617528c5740da24ec984ac282ee6.js"></script>
