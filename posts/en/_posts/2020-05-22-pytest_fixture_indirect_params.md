---
layout: post
lang: en
ref: pytest_fixture_indirect_params
title: "How to send params (indirectly) to pytest fixture from test"
comments: true
tags: [python, pytest, fixture]
---
![](/images/directindirect.png){:.post-title}

Pytest fixtures are params of a test. 
What if we want to change fixture behaviour for a test? 
How to send some params into a fuxture from a test?

I will show how to do that using fixture `data_path` as an example.

This fixture facilitates data files usage in pytest tests.

The fuxture looks fo data folder in the same folder as test itself. And with name
as the test module name with `_data`. Also the fixture copies all folder files into temp
folder so the test does not have a chance to corrupt them. The temp folder name is the
fixture value. 

Using this fixture you keep your test code clean without repeated data folder manipulations.

<script src="https://gist.github.com/andgineer/a238cba69c88466024e1f854082e4188.js"></script>

Now you can use the fixture:

    tests/
        conftest.py      # with fixture data_path
        foo_data/        # test data folder
            my_file.txt
        test_foo.py      # here is test `def test_foo` using folder `foo_data`

    def test_foo(data_path):
            my_file_path = data_path / "my_file.txt"
            with my_file_path.open() as data:
                ...
                
What if we want use the same folder for a tests from different test modules?
Or run test a number of times for different data files?

We have to pass this information into the fixture. For that we can use
[pytest indirect parameter](https://docs.pytest.org/en/latest/example/parametrize.html#apply-indirect-on-particular-arguments)

    tests/
        conftest.py         # with fixture data_path
        foo/                # test data folders
            1/              # data for 1st test run
                my_file.txt
            2/              # data for 2nd test run
                my_file.txt
        test_foo.py         # here is test `def test_foo` using folders `foo/1` and `foo/2`
        
    @pytest.mark.parametrize('data_path', ['foo/1', 'foo/2'], indirect=['data_path'])
    def test_foo(data_path):
            my_data_path = data_path / "my_file.txt"
            with my_data_path.open() as data:
                ...



