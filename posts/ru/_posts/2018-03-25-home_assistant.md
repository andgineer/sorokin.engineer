---
layout: post
lang: ru
ref: home_assistant
title: "Домашняя автоматизация с Xiaomi и Home assistant"
comments: true
tags: [smart home, Home asssitant]
redirect_from: "/posts/ru/home_assistant/"
---

### Введение

Для решения бытовых задач я купил [супер-дешевые устройства Xiaomi](https://www.aliexpress.com/wholesale?catId=0&initiative_id=SB_20180324195405&SearchText=xiaomi+mi+home)
для домашней автоматизации.
В минимальный набор должен входить Gateway, который уже умеет соединяться по протоколу zigbee
с остальными устройствами Xiaomi.
По сравнению с zigbee хабами, например, от samsung, это очень недорогое решение.


Устройства столь же великолепны и безпроблемны, сколь ужасен софт для них от Xiaomi.
Он в существенной степени не локализован, так что вы будете постоянно видеть половину экрана в иероглифах, он
неудобен и малофункционален, и он медленно работает (ну в чем смысл внопки в смартфоне, включающей свет,
если она вначале "открывается" примерно 15 секунд с надписью "инициализация zigbee - проще дойти до выключателя 
на стене)

Я попробовал OpenHAB, но мне кажется, что они сами не понимают, куда развиваются.
Дикое месиво между конфигами и малофункциональным UI, в котором невозможно разобраться, не прочитав 
вначале инструкцию по его использованию.

Также посмотрел на [Domoticz](https://www.domoticz.com/wiki/Main_Page) но он показался мне
не очень развивающимся и есть риск что его скоро совсем забросят.


### Home assistant
И тут на глаза попался [Home assistant](https://www.home-assistant.io).

С очень внятными инструкциями, как установить их docker-контейнер
[homeassistant/home-assistant](https://www.home-assistant.io/docs/installation/docker/) на NAS Synology.

Единственно, они почему-то не настаивают на смене пароля доступа
через http. Чтобы установить свой пароль, надо добавить в `configuration.yaml`:

    http:
      # Secrets are defined in the file secrets.yaml
      api_password: !secret http_password

И в файле `secrets.yaml` указать пароль в:

    http_password: <ваш пароль>

## Xiaomi

Для управления устройставми, подключенными к Xiaomi шлюзу надо добавить его ключ в конфигурацию
home assistant `configuration.yaml`:

    xiaomi_aqara:
      gateways:
        - mac: <MAC вашего шлюза>
          key: <key вашего шлюза>
          
          
Получение ключа - нетривиальные манипуляции с китайским приложением MiHome, описанные 
[у коллег из Domoticz](https://www.domoticz.com/wiki/Xiaomi_Gateway_(Aqara)#Adding_the_Xiaomi_Gateway_to_Domoticz).

Внятные имена вместо идентификаторов можно настроить в файле `customize.yaml`