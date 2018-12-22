---
layout: post
lang: en
ref: python_decorator_function_signature
title: "Python decorators - how to keep function signature (set of arguments) unchanged"
comments: true
tags: [Python decorator]
redirect_from: "/posts/en/python_decorator_function_signature.md/"
---
![](/images/decorator.jpg){:.post-title}
## Problem

[Decorators](https://docs.python.org/3/library/doctest.html) modify original
function.

As a result we have new function with different `sugnature` (set of
arguments).

Sometimes we want to keep old set of arguments.
For example if we use some tool that based on the function
arguments it will cease to work because new function will have
other set of arguments.
 
For example after:

{% highlight python %}
{% include src/decorator.py %}
{% endhighlight %} 

We will have only faceless `*args, **kwargs` as our new function arguments.

## How to save function arguments list after it had been decorated

In Python 3.3 and above 
([PEP0362](https://www.python.org/dev/peps/pep-0362/#visualizing-callable-objects-signature))
you can use special attribute `__signature__` to save original arguments list:

{% highlight python %}
{% include src/decorator2.py %}
{% endhighlight %}

## How to save other function attributes

The arguments list is not the only function feature that we lost after
our decorator.

For example we will loose also `__doc__` and that will be a problem for
[doc-tests](https://docs.python.org/3/library/doctest.html)  - all the 
doc-tests won't work anymore.

This and many other attributes of the function that had been decorated you can 
save with help of `wraps` from `functools`:

{% highlight python %}
{% include src/decorator3.py %}
{% endhighlight %}

It's a pity that for `__signature__` you need separate code and cannot use the 
same `wraps`. 

This is because many functions just do not have 
`__signature__` attribute. You have to create it with help of `inspect`.
`wraps` just copy existing attributes so it's no help there.
