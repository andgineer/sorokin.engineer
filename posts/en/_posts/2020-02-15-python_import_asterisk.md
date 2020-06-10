---
layout: post
lang: en
ref: python_import_asterisk
title: "Import all names from Python files in package (from * import *)"
comments: true
tags: [python]
---
![](/images/python_import.jpg){:style="float: left;margin-right: 7px;margin-top: 7px;"}

If you find yourself writing something like this in your `__init__.py` for each file you
add to the package

{% highlight python %}
from foo import *
from bar import *
{% endhighlight %}

I can give you small code snipped how to automate that.

But first - why do we write something like that at all?
In many cases this is just bad style  - you mix a lot of names in the namespace
and that can be dangerous. So in general you better avoid that.

But what about such a design

{% highlight python %}
- model.py
    - user.py
        class User(Base):
            ...
    - order.py
        class Order(Base):
            ...
{% endhighlight %}

For me I would prefer after that to do something like that

{% highlight python %}
- controllers.py
    - add_user.py
        import model
        def add_user(user: model.User):
            ...
{% endhighlight %}

but instead of that I have to write

{% highlight python %}
- controllers.py
    - add_user.py
        import model.user
        def add_user(user: model.user.User):
            ...
{% endhighlight %}

Ugly?

Ok we can add `__init__.py` so `model.User` would be possible:

{% highlight python %}
- model.py
    - __init__.py
        from .user import *
        from .order import *
    - user.py
        class User(Base):
            ...
    - order.py
        class Order(Base):
            ...
{% endhighlight %}

But this is just boring to write all this `import` for each model we add.

Stop! This is Python so you can automate all what you want!

This little code snippet solves exactly this task - how to `from * import *`.
<script src="https://gist.github.com/andgineer/141f97164aaea12215cf9a2aed332c1d.js"></script>

On line 8 we iterate all files in the folder using 
[Path.globe()](https://docs.python.org/3/library/pathlib.html#pathlib.Path.glob).

On line 9 we check this is not subfolder and the name is not starts with underscore 
(so we exclude `__init__.py` and all other files you give such a special names).

On line 10 we import the file as Python module using for that relative package name
(see dot at the beginning?).

Line 11 gets list of all non-magic names from the module.

And finally on line 12 we add all this names to the current namespace (`__init__.py`).
