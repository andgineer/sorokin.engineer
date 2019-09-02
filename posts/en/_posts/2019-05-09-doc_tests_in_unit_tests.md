---
layout: post
lang: en
ref: doctests_in_unittests
title: "Including doc tests into unit tests session"
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

## how to run doctests in your unit tests session

[doctest](https://docs.python.org/3.7/library/doctest.html) could be very convenient.
Mostly in cases if usage examples are the best tests for the code.

But if you add doc-tests in your project where you use [unitests](https://docs.python.org/3/library/unittest.html) 
you've got a problem - how to get just one test result.

If you want one result to see and to use in [CI](https://en.wikipedia.org/wiki/Continuous_integration)
you can include doc-tests into unit-tests session.

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


I use [load_tests protocol](https://docs.python.org/3/library/unittest.html#load-tests-protocol)
to create unit tests wrappers for doc tests and add them to the unit test session.

As a result we will have just one exit code, for unit tests and for doc tests.

Another bonus - more clear test report.
 