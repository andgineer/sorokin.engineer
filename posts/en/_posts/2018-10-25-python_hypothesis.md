---
layout: post
lang: en
ref: python_hypothesis
title: "Test Python with Hypothesis"
comments: true
tags: [python, test, hypothesis]
redirect_from: "/posts/ru/python_hypothesis/"
---
![](/images/hypothesis.jpg){:style="float: right;margin-right: 7px;margin-top: 7px;"}

<style type="text/css">
  h2 {
    content: "";
    clear: both;
  }
</style>

## Testing base on knowledge base

Each time you write test you straggle to choose good testing parameters.

There is temptation to use random values but it has some drawbacks.
Lack of repeatability for first. And in fact it is not so good to
find weak places in your application. You need a lot of runs to stumble upon
ingenious data - you know like in 
[Infinite monkey theorem](https://en.wikipedia.org/wiki/Infinite_monkey_theorem)

But do there is knowledge base for that just waiting for you use it.

{% highlight python %}
{% include src/test_finance.py %}
{% endhighlight %} 
    test_finance.py F
    test_finance.py:15 (test_bonus_distribution)
    1.0000000000000002 != 1.0
    
    Expected :1.0
    Actual   :1.0000000000000002

The example is very simple one just to give you a taste.
Of cause you know beforehand and without any tests that this code is bad one 
to manipulate with money. But just imagine some novice wrote it, used
Hypothesis to test and `bang!` - through Hipothesis she gets advice from experts 
that actually this is not so good code. 

Just think about that - this is not just test framework but expert knowledge base.
