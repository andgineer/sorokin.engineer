---
layout: post
lang: ru
ref: python_venv
title: "Работа с независимыми Python окружениями"
comments: true
tags: [python, virtualenv]
---
![](/images/workenv.png){:.post-title}

Уверен что вам нравится работать на удобном рабочем месте, где все под рукой и в порядке.

Чтобы не тратить часы на утомительные поиски что не так в вашем Python окружении, и как починить
библиотеку переставшую работать потому что вы поставили другую библиотеку, требуемую в каком-то из 
ваших проектов, есть простой способ, как поддерживать порядок.  

Теперь, начиная с [Python 3.6](https://docs.python.org/3.6/library/venv.html) это стало еще проще.
Раньше вам требовалось установить [virtualenv](https://virtualenv.pypa.io/en/latest/). 
Но теперь в лучших традициях python "батарейки в комплекте"!

    python3 -m venv <venv folder name>
    
Для Windows

    python -m venv <venv folder name>
    
Эта команда создаст в `<venv folder name>` "виртуальное окружение" где будут все используемые в этом
окружении библиотеки.

Чтобы "активировать" его (обратите внимание на `.` это сокращение для [source](https://superuser.com/questions/176783/what-is-the-difference-between-executing-a-bash-script-vs-sourcing-it))
    
    . <venv folder name>/bin/activate 
    
Для Windows

    <venv folder name>\Scripts\activate.bat

После активации будут использоваться Python библиотеки из из этого окружения. И когда вы что-то
устанавливаете с помощью `pip install` это меняет только это окружение и никак не испортит другие 
окружения или ваши глобальные настройки системы.    
    
Чтобы "выйти" из окружения

    deactivate    
    
Чтобы вам было еще проще этим пользоваться я написал скрипт `activate.sh`:

<script src="https://gist.github.com/andgineer/345eac0abb9149c165b64bf0d9c8694e.js"></script>

Он работает только в Linux и MacOS (обратите внимание на `.`)

    . ./acivate.sh
    
Скрипт создаст окружение если оно еще не создано. И установит вспе библиотеки перечисленные в файле 
`requirements.txt`. Если окружение уже было создано ранее то скрипт не будет его создавать
 повторно (см проверку на строке 25).
  
После этого скрипт активирует окружение (строка 32).
В переменной `PYTHON` (строка 7) в скрипте вы можете указать необходимую вам версию Python. 
При желении можно изменить и имя каталога `VENV_FOLDER` (строка 6).

Строки 14..22 проверяют что вы правильно вызвали скрипт с помощью [source](https://superuser.com/questions/176783/what-is-the-difference-between-executing-a-bash-script-vs-sourcing-it) (или сокращения `.`).

Если у вас возникнет ошибка `.. 'ensurepip', '--upgrade', '--default-pip']' returned non-zero exit status 1` 
скорее всего это означает что модуль `ensurepip` не установлен для нужной вам версии Python
(переменная `PYTHON`) и вы должны установить ее. Например для python3.7 в Ubuntu:

    sudo apt-get install python3.7-venv
