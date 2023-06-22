---
layout: post
lang: ru
ref: itunes_audiobook_from_mp3
title: "Аудиокниги iPhone из кривых mp3"
comments: true
tags: [ios, audiobook, python]
redirect_from: "/posts/ru/itunes_audiobook_from_mp3/"
---
![](/images/brothers_karamazov_ardis.jpg)

## Аудиокниги iTunes из mp3 файлов с кривыми тэгами
Вы попытались загрузить файлы аудиокниги в iTunes или какой-то плеер.

И видите что все mp3 тэги превратились в кракозябры, а порядок прослушивания стал совершенно произвольным, и
теперь книга может начинаться, например, с эпилога.

Это не зависит от того, откуда вы взяли файлы книги. У меня это происходит с книгами купленными и онлайн и на древних
CD-дисках.

## Как это починить

Установите [audiobook-tags](https://github.com/andgineer/itunes-audiobook-from-mp3)

Для этого у вас должен быть установлен [Python](https://www.python.org/downloads/).

    python -m pip install audiobook-tags

Чтобы конвертировать файлы, например в каталоге `~/Downloads/audiobook`:

    audiobook-tags ~/Downloads/audiobook -n=name

Эта команда поправит кодировку тегов, при условии что это Win1251 (если вам нужна другая, то используйте
аргументы `--encoding`). И отсортирует порядок по имени файла - если вам нужен другой порядок, то почитайте
описание аргумента `--num`.

Чтобы получить справку по программе используйте

        audiobook-tags --help

На этом все! Можно загрузить файлы, например в плеер [audible](http://www.audible.com) или любой другой, и слушать.

Мне, например, нравится плеер [evermusic](https://apps.apple.com/ru/app/evermusic-%D0%BE%D1%84%D1%84%D0%BB%D0%B0%D0%B9%D0%BD-%D0%B0%D1%83%D0%B4%D0%B8%D0%BE%D0%BF%D0%BB%D0%B5%D0%B5%D1%80/id885367198)
который вроде как есть и для Android.

## Создать аудиокнигу в iTunes

Если вы хотите создать аудиокнигу в iTunes, то после импорта файлов придется проделать еще следующий шаг.

Веделите файлы аудиокниги и выберите в свойствах информацию о файлах:

![](/images/itunes_media_kind.png)

укажите там, что это аудиокнига:

![](/images/itunes_media_kind_select.png)

тогда она переместится в раздел аудиокниг.
