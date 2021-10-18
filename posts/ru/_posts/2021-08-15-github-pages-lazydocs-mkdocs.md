---
layout: post
lang: ru
ref: 2021-08-15-github-pages-lazydocs-mkdocs
title: "Создание Github pages с помощью mkdocs и генерация документации по Python docstrings"
comments: true
tags: [python, guthub pages, jekyll]
---

![](/images/github-pages.jpeg){:.post-title}

# Простые github pages без Jekyll

[Github pages](https://pages.github.com) это отличный способ создать свой сайт.
Например данный сайт хостится на github pages.

В большинстве случаев для github pages используют [Jekyll](https://jekyllrb.com).
Это не такой уж сложный и мощный движок, если вам нужна какая-то логика, как, например, в этом блоге.

Но если вам надо опубликовать просто набор текстов, Jekyll вам просто ни к чему.

Чтобы создать сайт из каталога с файлами [markdown](https://www.markdownguide.org/basic-syntax/) можно использовать [mkdocs](https://www.mkdocs.org).
В том числе он сам умеет публиковать github pages.

А чтобы сгенерировать документацию по вашим исходникам можно использовать [lazydocs](https://github.com/ml-tooling/lazydocs).
Он даже вставит ссылки на точные строки, ведущие на вашу репу на github.

Движущихся частей у нас получилось много, чтобы вам не запутаться я и создал эту инструкцию.

# TL;DR

Используйте [aioS3 repo](https://github.com/andgineer/aios3) как шаблон для вашего проекта.

# Docstrings

Для генерации markdown файлов из ваших docstrings

    pip install lazydocs
    mkdir -p /docs/docstrings

    lazydocs \
        --output-path="./docs/docstrings" \
        --overview-file="README.md" \
        --src-base-url="https://github.com/<you github account>/<your repo>/blob/master/" \
        <folder with source code>

Это создаст markdown файлы в каталоге `docs/docstrings`.

# mkdocs

    pip install mkdocs mkdocs-awesome-pages-plugin

Создайте конфиг `mkdocs.yml` в корне вашей репы

    site_name: <your site name>
    site_url: https://<you github account>.github.io/<your repo>
    site_author: <you name>

    # Repository
    repo_name: <your repo>
    repo_url: https://github.com/<you github account>/<your repo>
    edit_uri: edit/master/docs
    docs_dir: docs

    plugins:
        - awesome-pages
        - search

    theme:
      name: readthedocs

Плагин `awesome-pages` используется для инстеграции с lazydocs.
Не создавайте секцию `nav` - она будет создана автоматически.

Я использую тему `readthedocs`. Конечно, вы можете выбрать что угодно
[используя mkdocs](https://www.mkdocs.org/user-guide/choosing-your-theme/).

mkdocs создает сайт из каталога с markdown файлами.
Мы сгенерили каталог `docs/docstrings` из исходников. 

Теперь вы можете добавить любые markdown файлы в каталог `docs/`. 
Если вам надо указать в них ссылки на сгенерированные доки то можно использовать ссылки вида

    Используя aioS3 [stream()](docstrings/file/#function-stream) ...

Здесь `file` - имя файла без расширения, а `stream` - имя функции в нем.

mkdocs использует как входную страницу либо `index.md` либо `README.md`.

Чтобы локально посмотреть что у нас получилось

    mkdocs serve

# github pages

В настройках репы github укажите публикацию из ветки `gh-pages`.

![](/images/github-settings-pages.png)
    
Эта ветка создается и наполняется командой

    mkdocs gh-deploy

# github actions

Чтобы доки у нас создавались и публиковали автоматически задействуем gihhub action.
Не пугайтесь - для этого надо всего лишь создать пару файлов.

В корне создаем `build-docs.sh`

    #!/usr/bin/env bash
    lazydocs \
        --output-path="./docs/docstrings" \
        --overview-file="README.md" \
        --src-base-url="https://github.com/<you github account>/<your repo>/blob/master/" \
        <folder with source code>
    
    mkdocs build

А в каталоге `.github/workflows/` создаем `docs.yml`

    name: docs
    on:
      push:
        branches:
          - main
          - master
    jobs:
      deploy:
        runs-on: ubuntu-latest
        steps:
          - uses: actions/checkout@v2
          - uses: actions/setup-python@v2
            with:
              python-version: 3.x
          - run: |
              pip install lazydocs mkdocs mkdocs-awesome-pages-plugin
          - run: ./build-docs.sh
          - run: mkdocs gh-deploy --force

Теперь ваши github pages будут автоматически создаваться из ваших Python docstrings и markdown файлов, которые вы добавите руками.
Ваш сайт будет доступен на `https://<you github account>.github.io/<your repo>`.
