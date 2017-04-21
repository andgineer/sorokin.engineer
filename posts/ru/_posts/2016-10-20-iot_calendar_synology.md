---
layout: post
lang: ru
ref: iot_calendar_synology
title: "Отображение на kindle событий умной wi-fi кнопки (Synology)"
comments: true
summary: ... календарь собыйти кнопки ...
tags: [amazon dash button, python, docker, synology]
---

В статье [Умная wi-fi кнопка и Docker на Synology](http://masterandrey.com/posts/ru/amazon_dash_button_hack/)
описано, как вы можете регистрировать в Google Calendar события от кнопки Amazon Dash Button.

Ниже рассказывается, как показать этот календарь на вашем старом Kindle, который вы можете повесить на стену.

Конечно, календарь можно вывести и на компьютер или планшет. Например, всего за $49 ($39 на регулярно проводимых
распродажах) вы можете купить Amazon Fire HD 7. Или, за сравнимые деньги, недорогой китайский планшет.
Но чтобы он висел на стене постоянно включенным, вам надо подводить к нему питание и решать вопрос работы без батареи
(потому что батарея в режиме постоянно подключения все равно быстро деградирует).

## Установка на Synology

Вы можете вместо выполнения описанной ниже инструкции импортировать 
[мои настройки контейнера](https://github.com/masterandrey/docker-iot-calendar/tree/master/synology).
Они предполагают, что [файлы с секретами и настройками](https://github.com/masterandrey/docker-iot-calendar/tree/master/amazon-dash-private)
вы разместили на своем Synology в каталоге `docker/amazon-dash-private`.
![](/images/synology_import_settings.png)

Ниже же описано, как сделать все это самостоятельно.

Добавляем в Docker image с моим приложением `https://hub.docker.com/r/masterandrey/docker-iot-calendar/`:

![](/images/dash_synology_docker_image.png)
![](/images/dash_synology_docker_url.png)

Когда он скачается, чтобы создать из него контейнер, два раза кликните по нему.

В `Advanced settings` -> `Volume` подключите к контейнеру каталог `/amazon-dash-private` с секретами доступа к 
календарю Google и прочими настройками приложения.
Скачайте [примеры этих файлов](https://github.com/masterandrey/docker-iot-calendar/tree/master/amazon-dash-private) 
и разместите в любом удобном вам месте на Synology.

Например, у меня они находятся на томе Synology в каталоге 
`docker/amazon-dash-private`:

![](/images/dash_synology_docker_volume.png)

А в `Port Settings` сделайте видимым снаружи порт `4444`, на котором работает приложение.

![](/images/calendar_synology_docker_port.png)

В `Package Center` отключите автообновление Docker.
Поскольку после автообновления не перезапускаются контейнеры и ваши кнопки неожиданно перестанут работать.
Лучше обновлять вручную и перезапускать нужные контейнеры.

![](/images/dash_synology_docker_autoupdate.png)

## Не Synology

Вам надо положить `amazon-dash-hack.json` и прочие файлы в каталог 
`amazon-dash-private` и добавить в командную строку docker:

    -v $PWD/amazon-dash-private:/amazon-dash-private:ro
    
$PWD в данном случае говорит о том, что каталог `amazon-dash-private` размещен в том же каталоге,
в котором вы запускаете docker. Если это не так, то измените это соотвествующим образом.

## Календарь событий

По адресу `<ваш сервер>:4444` теперь доступен перечень настроенных в вашем файле `settings.json` дашбордов
(`dashboards`).

`<ваш сервер>:4444?b=<идентификатор дашборда>` покажет страницу с черно-белым вариантом календаря,
`<ваш сервер>:4444?b=<идентификатор дашборда>&style=seaborn-talk` с цветным. В эту страницу встроен
скрипт который вызывает ее авто-обновление.

Само изображение можно получить `<ваш сервер>:4444/dashboard.png?b=<идентификатор дашборда>` или
`<ваш сервер>:4444/dashboard.png?b=<идентификатор дашборда>&style=seaborn-talk` для черно-белого
и цветного соответственно.
