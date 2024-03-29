---
layout: post
lang: ru
ref: iot_calendar_synology
title: "Отображение на Kindle календаря IoT (wi-fi кнопки)"
comments: true
tags: [amazon dash button, python, docker, synology]
redirect_from: "/posts/ru/iot_calendar_synology/"
---

![](/images/dashboard.png)

В статье [Умная wi-fi кнопка](/posts/ru/amazon_dash_button_hack.html)
описано, как вы можете регистрировать в Google Calendar события от кнопки Amazon Dash Button.

Ниже рассказывается, как показать этот календарь на вашем старом Amazon Kindle, который вы можете повесить на стену.

Конечно, календарь можно вывести и на компьютер или планшет. Например, всего за $49 ($39 на регулярно проводимых
распродажах) вы можете купить Amazon Fire HD 7. Или, за сравнимые деньги, недорогой китайский планшет.
Но чтобы он висел на стене постоянно включенным, вам надо подводить к нему питание и решать вопрос работы без батареи
(потому что батарея в режиме постоянно подключения все равно быстро деградирует).

## Настройки

Помимо настройки кнопок в `settings.json` и `buttons.json`, описанной в 
[Установка на Synology умной wi-fi кнопки](/posts/ru/amazon_dash_button_hack_install.html),
вам необходимо настроить параметры отображения событий.

Это делается в разделе `dashboards`. Настраивается картинка для дней, в которых не было событий `empty_image` (т.е.
дни, которые прогуляли). Также в календаре можно отмечать уважительные отсутствия (как события описанные в 
`absents`, для них в прогулянные по событиям от кнопки дни будут отображаться другие картинки).
Например, если имеется в `absent` элемент с `summary` равным `Sick`, и вы введете в календарь кнопки
событие с таким названием, то в течение этого события вместо `empty_image` будет показываться картинка,
указанная в этом элементе.

Поскольку на календаре также показывается погода (раз уж висит на стене Kindle, пусть и погоду тоже показывает),
то, если вам хотелось бы видеть местную погоду, а не погоду в Питере, надо настроить ваши географические координаты.
Сделать это можно с помощью [карт Google](https://support.google.com/maps/answer/18539?co=GENIE.Platform%3DDesktop&hl=ru).
Полученные координаты укажите в `settings.json` в параметрах `latitude` и `longitude`.

Также вам надо получить 
[ключ API openweathermap](https://home.openweathermap.org/users/sign_up) и поместить его в файл
`openweathermap_key.json` вместе с остальными файлами настроек (при желании можете изменить путь к этому файлу
в параметре `openweathermap_key_file_name` в `settings.json`).

## Установка на Synology

Добавляем в Docker image с моим приложением [iot-calendar](https://hub.docker.com/r/andgineer/iot-calendar):

![](/images/dash_synology_docker_image.png)
![](/images/dash_synology_docker_url.png)

Когда он скачается, можно создавать Docker контейнер из этого image.

Вы можете вместо выполнения описанной ниже инструкции импортировать 
[мои настройки контейнера](https://github.com/andgineer/docker-iot-calendar/tree/master/synology).
Они предполагают, что [файлы с секретами и настройками](https://github.com/andgineer/docker-iot-calendar/tree/master/amazon-dash-private)
вы разместили на своем Synology в каталоге `docker/amazon-dash-private`.
![](/images/synology_import_settings.png)

Ниже же описано, как сделать все это самостоятельно.

Два раза кликните по скачанному image, это запустит процесс создания контейнера Docker.

В `Advanced settings` -> `Volume` подключите к контейнеру каталог `/amazon-dash-private` с секретами доступа к 
календарю Google и прочими настройками приложения.
Скачайте [примеры этих файлов](https://github.com/andgineer/docker-iot-calendar/tree/master/amazon-dash-private) 
и разместите в любом удобном вам месте на Synology.

Например, у меня они находятся на томе Synology в каталоге 
`docker/amazon-dash-private`:

![](/images/calendar_synology_docker_volume.png)

А в `Port Settings` сделайте видимым снаружи порт `4444`, на котором работает приложение.

![](/images/calendar_synology_docker_port.png)

В `Package Center` отключите автообновление Docker.
Поскольку после автообновления не перезапускаются контейнеры и ваши Docker приложения неожиданно перестанут работать.
Лучше обновлять вручную и перезапускать нужные контейнеры.

![](/images/dash_synology_docker_autoupdate.png)

## Не Synology

Вам надо положить `amazon-dash-hack.json` и прочие файлы в каталог 
`amazon-dash-private` и добавить в командную строку docker:

    -v $PWD/amazon-dash-private:/amazon-dash-private:ro
    
$PWD в данном случае говорит о том, что каталог `amazon-dash-private` размещен в том же каталоге,
в котором вы запускаете docker. Если это не так, то измените это соотвествующим образом.

## Календарь событий

Откройте в браузере `<ваш сервер>:4444`, вы увидете список настроенных в вашем файле `settings.json` 
дашбордов (`dashboards`).

`<ваш сервер>:4444?b=<идентификатор дашборда>` покажет страницу с черно-белым вариантом календаря,
`<ваш сервер>:4444?b=<идентификатор дашборда>&style=seaborn-talk` с цветным. В эту страницу встроен
скрипт который вызывает ее авто-обновление.

Само изображение можно получить `<ваш сервер>:4444/dashboard.png?b=<идентификатор дашборда>`.
 
По умолчанию оно черно-белое и повернуто на 90 градусов, для лучшего показа на Kindle. При желании, вы можете выбрать другие
стили (они влияют, на цветовую гамму, шрифты, дизайн осей графиков и пр.).
Поддерживаемые стили можно посмотреть например 
[тут](https://tonysyu.github.io/raw_content/matplotlib-style-gallery/gallery.html).
Например, `<ваш сервер>:4444/dashboard.png?b=<идентификатор дашборда>&style=seaborn-talk&rotate=0`.

Также можно выключить включенный по умолчанию рукописный стиль `xkcd=0` (этот стиль накладывается
после описанного выше основного стиля и изменяет ряд параметров отображения).

Если вам не нравятся пиктограммы которое я использую при рисовании календаря, вы можете выбрать
любые другие, например, на 
[Noun Project](https://thenounproject.com).