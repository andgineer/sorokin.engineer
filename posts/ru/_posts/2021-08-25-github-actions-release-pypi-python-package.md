---
layout: post
lang: ru
ref: 2021-08-25-github-actions-release-pypi-python-package
title: "Автоматическая публикация пакетов pip package по тегу git и создание github release"
comments: true
tags: [python, guthub actions, git]
---

![](/images/pip.jpg){:.post-title}

# Github action для создания пакета PIP и создания Github release

Если у вас есть пакет PIP, то вам необходимо установить связь между версией исходных текстов и
версией на pypi.org.

Для этого недостаточно просто записать git commit. Потому что вручную вы може опубликовать PIP версию в любой момент.

Один из подходов - использовать git tag, всегда публиковать на pypi только по тегу.
Это обеспечит жесткую связь версии в git и на pypi.

Для этого можно использовать Github actions.

# Что вы получите

Запуская `./verup.sh bug/feature/release`
- увеличивается младшая/средняя/старшая цифра в версии в теге
- обновляется версия в файле `version.py` внутри вашего пакета
- эта версия публикуется для PIP (pypi.org)
- создается Github release со ссылкой на соотвествующую страничку версии на pypi

# Адаптация под ваш проект

Как шаблон возьмите [aioS3 repo](https://github.com/andgineer/aios3).

## activate.sh

Перед началом работы всегда запускайте

    . ./activate.sh

Обратите внимание на первую `.` - она обеспечивает возможность активации виртуального окружения Python.
Если окружение еще не существует, то скрипт его создаст.

Если вам необходимо обновить зависимости вы можете просто удалить окружение `rm -r venv`. 
При следующем запуске `activate.sh` оно вновь создастся с последними версиями зависимостей.

[activate.sh](https://github.com/andgineer/aios3/blob/master/activate.sh) 
также устанавливает ваш пакет в режиме разработчика `pip install -e .` так что то что выимпортируете будет
текущей версией исходников.

Если вы, как и я, описываете зависимости в [requirements.txt](https://github.com/andgineer/aios3/blob/master/requirements.txt) 
то вам ничего не нужно менять в этом файле.

Но не забудбте установить [virtualenv](https://virtualenv.pypa.io/en/stable/installation.html) необходимый для его работы.

# setup.py

Вместо `aios3` в строке [from src.aios3 import version](https://github.com/andgineer/aios3/blob/19b3a6b4b6904883fa8a3a25e474983a1563b02e/setup.py#L9) 
укажите название вашего пакета. 

Свой пакет поместите в `src/`.
PIP автоматически найдет все пакеты в каталоге `src`.

# verup.sh

Используйте `verup.sh` для создания тегов с версиями, никогда не создавайте их вручную.

Версия состоит из трех цифр:

    release.feature.bug

Например, для изменения последней запустите

    ./verup.sh bug

А для изменения первой

    ./verup.sh release

Этот скрипт также обновляет `version.py`.
Вы можете этот модуль в своем приложении, чтобы показывать версию.

Также этот файл используется в `setup.py` для определения пуьликуемой на `pypi.org` версии.

Не забудьте поправить в [VERSION_FILES](https://github.com/andgineer/aios3/blob/19b3a6b4b6904883fa8a3a25e474983a1563b02e/verup.sh#L5) 
в файле `verup.sh` пути к этому файлу. Если нужно создавать несколько файлов с версией (например, если у вас несколько пакетов в `src/`), 
то можно перечислить несколько путей, разделенных пробелами.

# Github action .github/workflows/pip_publish.yml

В строке [body: https://pypi.org/project/aios3/${{ env.RELEASE_VERSION }}/](https://github.com/andgineer/aios3/blob/19b3a6b4b6904883fa8a3a25e474983a1563b02e/.github/workflows/pip_publish.yml#L47) 
измените `aios3` на название вашего пакета.

