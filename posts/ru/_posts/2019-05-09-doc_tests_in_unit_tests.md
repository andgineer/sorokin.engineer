---
layout: post
lang: ru
ref: doctests_in_unittests
title: "Включение doc tests в сессию unit tests"
comments: true
tags: [python, test, doctest, unittest]
---
![](/images/python_doctest.jpeg){:style="float: right;margin-right: 7px;margin-top: 7px;"}

<style type="text/css">
  h2 {
    content: "";
    clear: both;
  }
</style>

## Как включить doctests в сессию unittests

Иногда бывает очень удобно использовать [doctest](https://docs.python.org/3.7/library/doctest.html).
Я это делаю в тех ситуациях, когда пример использования становится одновременно самым удачным тестом.

Но если у вас есть также набор [unitests](https://docs.python.org/3/library/unittest.html) 
то мы получаем два набора тестов, что неудобно и с точки
зрения быстрого определения успешности и с точки зрения включения в [CI](https://en.wikipedia.org/wiki/Continuous_integration).

Чтобы устранить это неудобство мы можем добавить doc-tests в сессию unit-tests.

{% highlight python %}
import doctest
from os.path import dirname, basename, isfile
from glob import glob
from importlib import import_module

import mypackage
PACKAGES = [mypackage]  # list of packages where to find doc-tests

PY_EXT = '.py'  # in what files we will look for doc-tests


def load_tests(loader, tests, ignore):
    for package in PACKAGES:
        for module_file in glob(dirname(package.__file__) + f'/*{PY_EXT}'):
            if isfile(module_file) and not module_file.endswith('__init__.py'):
                tests.addTest(doctest.DocTestSuite(
                    import_module(f'{package.__name__}.{basename(module_file)[:-len(PY_EXT)]}')
                ))
    return tests
{% endhighlight %} 


Мы используем [load_tests protocol](https://docs.python.org/3/library/unittest.html#load-tests-protocol).
И добавляем к unit tests также создаваемые нами unit-test обертки для doc tests.

В итоге результат тестовой сессии unit test будет для всех тестов сразу, как обычных unit tests
так и doc tests.

Еще одно получаемое нами преимущество - более структурированный отчет о тестах.
 