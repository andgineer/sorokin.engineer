---
layout: post
lang: en
ref: python_super
title: "Python Multiple inheritance and super() function for dummies"
comments: true
tags: [Python]
redirect_from: "/posts/en/python_super/"
---

<style type="text/css">
  h2 {
    content: "";
    clear: both;
  }
</style>

Multiple inheritance is a feature in which a class can inherit characteristics 
from more than one parent class.

If we want to add the same methods to a number of classes we can do that
by copying methods to each class, but this is against 
[DRY principle](https://wikipedia.org/wiki/Don’t_repeat_yourself).

Also we can do that with
[decorators](https://www.python.org/dev/peps/pep-0318/)
but this is not convenient for big amount of application logic.

The better solution in this case - use
 [mixin](https://wikipedia.org/wiki/mixin), for Python it's multiple
 inheritence.


## Puzzle

{% highlight python %}
{% include src/animal_mro_without_super.py %}
{% endhighlight %}

First parent of `PlatypusMammalFirst`, `Platypus` (`Mammal`),
does not change the method we are looking for. 
But the second - (`Bird`) does. What `lay_eggs()` will print?

And what it will print for `PlatypusBirdFirst`?
Solution see below.


## Diamond problem
![](/images/object_diamond_uml.png){:style="float: right;margin-right: 7px;margin-top: 7px;"}
    
The puzzle above based on 
([diamond problem](https://en.wikipedia.org/wiki/Multiple_inheritance#The_diamond_problem)),
this is feature of multiple inheritance as it is, not for Python only.

As you can see on picture, if a number of classes has the same parent and the
same child, inheritance tree will have 'diamonds' (rhombs).

In Python 3 all classes without parent in fact inherits from 
`object`, so any case of multiple inheritance in Python 3 has diamonds in 
inheritance tree because of the common parent - `object`.


## C3 Algorithm Python 3 (MRO)
![](/images/diamond_uml.png){:style="float: right;margin-right: 7px;margin-top: 7px;"}

To look for inherited methods and attributes, Python use 
[C3 MRO algorithm](https://en.wikipedia.org/wiki/C3_linearization).

MRO stands for "method resolution order".

Very simple C3 explanation:

* add to the list all object's parents

  * to the end of the list add parent's parents
  * repeat
  
* if some class added more ones we remove all the occurrences 
except last one.

As a result we have search order in which we look for inherited methon
by parent layers - we do not look deeper before we look in all upper
layer parents.

For example for class `Platypus`, MRO: `[Mammal, Bird, Dinosaur, Vertebrate]`.
So we look in `Mammal`, `Bird`, `Dinosaur` first. 
And only after that - in `Vertebrate`.

C3 gives you overridden method if it is overridden in any of ancestors
despite their order in inheritance list of your class.

So the puzzle solution for Python 3 - `True` in both cases, we never get 
`None` from `Vertebrate`.

Python 2 use other MRO algorithm (`deep first`).
It drills deeper and deeper to the end of hierarchy for each parent by their
order in inheritance list.

Python 2 MRO: `[Mammal, Vertebrate, Bird, Dinosaur]`.
So after `Mammal` if will look into `Vertebrate`. 
And puzzle solution for Python 2 - `None` and `True`.

But in Python 2 we can use `new-style classes` and in this case it use the 
same `C3 MRO` as Python 3. To use `new-style` classes in Python 2 you should 
inherit `Vertebrate` from `object`. 
In Python 3 this is default - if a class inheritance list is empty
the class inherits from `object`.

With MRO as in Python 2 (`deep first`), we could not use multiple inheritance
at all because of this Python 3 feature - default parent `object`. 
So in Python 3 we always have diamond in inheritance tree for objects with
multiple inheritance because all classes have the same grad-..-grand parent.


## super() function

Function super() implements cooperative inheritance.

Do not be fooled by the name - `super()` it is not class parent!
This is class next by MRO list. 

As we will see below it can be sibling class.
And a class behaviour will change if we add it to different classes.

In some cases this is just intuitively right and good.
But that can be very confusing in other cases and can be a source of hard
to discover bug.

![](/images/animal_class_tree_uml.png){:style="float: right;margin-right: 7px;margin-top: 7px;"}

## Cooperative multiple inheritance with super()

{% highlight python linenos %}
{% include src/animal_class_tree.py %}
{% endhighlight %}
[... Execute ...](https://trinket.io/python3/87415de54d){:target="_blank"}{:style="background-color: WhiteSmoke;text-align: center;border: 1px solid silver;display: inline-block;width: 100%;"}

    Platypus.__init__()
    Mammal.__init__()
    Bird.__init__()
    Vertebrate.__init__()


'Cooperative' means everybody has to follow rules.
 
If any of child class won't call `super()`), parent method won't be
called at all even if we see that some other child do call parent.

For example lets remove `super()` call from `Bird` (line 8 in the listing above). 
We will have different results:

    Platypus.__init__()
    Mammal.__init__()
    Bird.__init__()
    
This is because in fact `Mammal.__init__` call next in MRO list class
(`Bird`), and not the parent `Mammal` (`Vertebrate`). 
The parent was called by `Bird`, but we removed that call.

In the code below I added args into `__init__`, so the error looks more obvious.

{% highlight python linenos %}
{% include src/animal_class_tree_arguments.py %}
{% endhighlight %}
    Platypus.__init__()
    Mammal.__init__()
    ...
    File "animal_class_tree_arguments.py", line 13, in __init__
        super().__init__()
    TypeError: __init__() missing 1 required positional argument: 'beak_length'

Now we see that in `Mammal` the line `super().__init__()` calls `Bird.__init__`.


#### Remarks about super()

Another contr-intuitive `super()` feature is unsupported
[binary operations](https://docs.python.org/3/reference/expressions.html#binary-arithmetic-operations) -
[subscriptions](https://docs.python.org/3/reference/expressions.html?highlight=slice#subscriptions)
etc.

Even if parent implements all necessary
["magic methods"](https://docs.python.org/3/library/operator.html)
it won't work in `super` calls. 

Example below illustrates that for `magic method` `__getitem__`, 
for operator `[]`.

It works in child but not in `super()`:

{% highlight python %}
{% include src/super_operations.py %}
{% endhighlight %}

    kid[0]: 0
    ...
    TypeError: 'super' object is not subscriptable
