---
layout: post
lang: ru
ref: pytest_fixture_indirect_params
title: "Передача параметров из теста в фикстуру pytest (indirect fixture params)"
comments: true
tags: [python, pytest, fixture]
---
![](/images/directindirect.png){:.post-title}

Фикстуры в pytest указываются как параметры функции-теста. Это означает что вы не можете
напрямую передать в них параметры.

Но что если в тесте вам необходимо чуть изменить поведение фикстуры?

Ниже я показываю, как это сделть, на примере фикстуры `data_path`.

Эта фикстура упрощает использование в тестах файлов с данными.

Она берет эти файлы из каталога, имя которого определяется именем модуля с тестом, добавляя к 
нему `_data`. И копирует эти файлы во временный каталог, возвращая его имя. Теперь у теста копия
данных и он точно их никак не испортит. 

К тому же это делает код теста чище - не нужно химичить со всеми этими `__file__` или
как-то иначе вычислять место файлов с тестовыми данными.

<script src="https://gist.github.com/andgineer/a238cba69c88466024e1f854082e4188.js"></script>

Теперь вы можете положить файл с данными в тот же каталог что модуль теста:

    tests/
        conftest.py  # здесь код фикстуры data_path
        foo_data/    # каталог с файлами для теста 
        test_foo.py  # здесь тест `def test_foo` использующий файлы из каталога `foo_data`

И использовать в тесте такой код:

    def test_foo(data_path):
            my_file_path = data_path / "my_file.txt"
            with my_file_path.open() as data:
                ...
                
Но что если нам хочется в тестах в разных модулях использовать один и тот же каталог с данными?
Или мы хотим повторить тест несколько раз для разных каталогов с даннами?

Для этого надо каким-то образом передать в фикстуру эту информацию.
Для этого можно использовать 
[pytest indirect parameter](https://docs.pytest.org/en/latest/example/parametrize.html#apply-indirect-on-particular-arguments)

Например, вот так

    tests/
        conftest.py  # здесь код фикстуры data_path
        foo/         # каталоги с файлами для теста 
            1/       # каталог с данными для первого прогона теста
            2/       # каталог с данными для второго прогона теста
        test_foo.py  # здесь тест `def test_foo` использующий файлы из каталогов `foo/1` и `foo/2` 
        
    @pytest.mark.parametrize('data_path', ['foo/1', 'foo/2'], indirect=['data_path'])
    def test_data(data_path):
            my_data_path = data_path / "mydata.txt"
            with my_data_path.open() as data:
                ...



