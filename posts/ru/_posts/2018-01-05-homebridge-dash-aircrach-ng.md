---
layout: post
lang: ru
ref: airdump
title: "Быстрая реакция кнопки Amazon Dash с помощью aircrack"
comments: true
tags: [MacOS aircrack amazon_dash_button]
---

![](/images/)

С помощью хака [AirCrack-ng](https://www.aircrack-ng.org) можно заставить кнопки от 
Amazon работать еще быстрее.

### Установка на Ubuntu Linux

    sudo apt-get install aircrack-ng
    
### Установка на MacOS

    brew install aircrack-ng
    PATH=${PATH}:/usr/local/sbin
    airodump-ng-oui-update
    
### Библиотека для Python

    sudo -H pip3 install pyrcrack
    
Конечно, если вы уже в режиме супер-пользователя, то `sudo -H` вам ни к чему.

И если pip у вас только для третьего Python то можно просто `pip` вместо `pip3`.

### Проверка, что все работает

    import pyrcrack.management
    with pyrcrack.management.Airmon('wlan0') as f:
      print(f.interface)