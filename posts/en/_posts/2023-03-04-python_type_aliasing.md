---
layout: post
lang: en
ref: python_type_aliasing
title: "Generic type aliasing in Python"
comments: true
tags: [Python, mypy, class]
---

![](/images/safari.jpeg){:.post-title}

### How to fix mysterious Python error `Mypy: expects no type arguments, but 1 given [type-arg]`

Have you ever heard of generic type aliases? 

At first glance, [the theory behind them](https://mypy.readthedocs.io/en/stable/generics.html#generic-type-aliases)
may seem complicated, but let me give you a practical example to make things easier to understand.

Imagine you have some generic list of animals. 
For example to encapsulate a function `escaped()` that apply to list of any animals.

Now let's say that you want to create specialized list of birds, list of reptiles, and so on. 

The problem is that you still want to use the common code for a generic list of animals. 
You also want to make sure that the types of animals in each list are checked, so that mypy won't allow you 
to add a bird to the list of reptiles.

_Alright, so I'm familiar with dinosaurs and all that, but let's not get too deep into it 
and just keep things simple for the sake of the conversation. 
We don't need to generalize everything over millions of years, ya know?
After all flying dinosaurs are not birds._


Write extremely simple code.. and hit some crazy mypy error message:

{% highlight python %}
{% include src/type_aliasing_initial.py %}
{% endhighlight %}

WTF? What is `[type-arg]` and why we can use `List[Bird]` but not `AnimalList[Bird]`?

When you use `List[Animal]` you actually use list with specific items types and without type argument that has its parent, generic `list`.

That's why now there is just no place where to specify type for `AnimalList` items, this is not generic list anymore.

The solution is extremely simple. Create type alias for `Animal`. 
In this case `AnimalList` still expect items type argument.

{% highlight python %}
{% include src/type_aliasing.py %}
{% endhighlight %}

If you think this is too abstract problem, you can look into [my code](https://github.com/andgineer/goodreads-export/blob/7b19c1f500e26e5d70dcbfd709f130f83be212f5/src/goodreads_export/templates.py#L150)
where I use this technique.

Curious about `bound` argument of `TypeVar` in the code above?
It just means that type specified by this alias could be `Animal` or subclass of `Animal`.
