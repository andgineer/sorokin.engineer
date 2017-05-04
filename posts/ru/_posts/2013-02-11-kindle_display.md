---
layout: post
lang: ru
ref: kindle_display
title: "Kindle keyboard as display"
comments: true
summary: ...Изпользование kindle как дисплея...
tags: [osx, kindle]
---

![](/images/kindle_dashboard.png)

## Подготовка Kindle

Прежде всего получаем root (установить пакет `kindle-jailbreak`):
[Font, ScreenSaver & USBNetwork Hacks for Kindle 2.x, 3.x & 4.x](https://www.mobileread.com/forums/showthread.php?t=88004).

У меня Kindle keyboard (Kindle 3) 3g, поэтому здесь и далее я использую 
файлы с `k3g_3.2.1` в имени.

Также устанавливаем screen saver hack (kindle-ss).

Чтобы открывались созданные сообществом Kindlets (в частности, описанный
ниже  KUAL), надо установить
[Mobileread Kindlet Kit (mkk)](https://www.mobileread.com/forums/showthread.php?t=233932)
который обеспечивает запуск этих неподписанных "документов".

В качестве запускалки хаков и своих приложений удобно использовать
[KUAL](https://www.mobileread.com/forums/showthread.php?t=251143),
чтобы его запустить на Kindle надо открыть соотвествующий "документ" KUAL.

Для ssh доступа к Kindle (как по USB проводу так и через WiFi) ставим
[USBNetworking](https://www.mobileread.com/forums/showthread.php?t=88004),
он появится как кнопка в KUAL.
 
Старые инструкции по USBNetworking полны описаниями магии
с набором на клавиатуре Kindle `<Del>`, `;debugOn` и так далее, но через
KUAL все это делается более безболезненно.
Просто заходим на Kindle в KUAL "документ" и включаем USB networking.

Важно - при любых переключениях USB networking надо отключать USB-кабель
от Kindle. Впрочем, в USBNetworking уже встроили защиту, и если этого
не соблюдать, то он напишет, что кабель надо отключить.

Также в KUAL -> USBNetworking включаем запуск ssh при перезагрузке и 
перегружаем Kindle.

В MacOS, Kindle со включенным USBNetworking появится в Network 
preferences как `RNDIS\...`. В этом сетевом интерфесе надо отключить
DHCP и указать для него Mac адрес `192.168.2.1`, сеть `255.255.255.0`.
У Kindle Keyboard при этом будет адрес `192.168.2.2` (как я понимаю,
адрес зависит от модели Kindle).

## SSH

Для авторизации через ssh надо
[вычислить пароль root](https://www.hardanswers.net/amazon-kindle-root-password)

Для безопасной авторизации лучше сгененировать SSL ключи

    ssh-keygen -C "AnSo Kindle developer key" -f id_anso_kindle
    scp id_anso_kindle.pub root@192.168.2.2:/mnt/us/usbnet/etc/authorized_keys/
    
и теперь можно 

    ssh -i id_anso_kindle.pub root@192.168.2.2
    
и при запросе пароля просто нажать `ENTER`.


## Использование kindle как дисплей

Интересный проект
[Online screensaver extension](https://www.mobileread.com/forums/showthread.php?t=236104)
Он только для Kindle touch

    not gonna work. Besides the limitations of the busybox shell shipped with the K3, which you're just starting to feel the pain of, the whole system expects & uses the framework of FW 5.x, which is, in that regard in particular, way, way, way different than FW 2.x/3.x/4.x.

    So, besides rewriting the script itself to play nice with the K3 busybox, 
    you'll also need to adapt the logic to fit your target device 
    (and be warned that it might not be 100% doable).

Вроде он делает ровно то, что надо - показ на весь экран, в режиме сна,
по таймеру включает wifi и обновляет screensaver.


[KOReader](https://github.com/koreader/koreader/wiki)

## Настройки режимов Kindle

### Чтобы kindle не засыпала

    <Del> to open the search box on the home screen
    ;debugOn <Enter>
    <Del>
    ~disableScreensaver <Enter>

Как побочный эффект, выключить kindle кнопкой тоже не получится.
Чтобы восстановить режим засыпания надо ввести

    <Del>
    ~resumeScreensaver <Enter>
    
И можно выйти из отладочного режима:

    <Del>
    ;debugOff <Enter>

### Скрыть статус-бар

[Hiding the status bar](https://www.mobileread.com/forums/showthread.php?t=207872&page=2)

    lipc-set-prop com.lab126.pillow disableEnablePillow disable
    lipc-set-prop com.lab126.pillow disableEnablePillow enable
    
Другой вариант

    wmctrl -r L:C_N:titleBar_ID:system -e '0,0,0,600,1' 
    wmctrl -r L:C_N:titleBar_ID:system -e '0,0,0,600,1' (twice since Awesome is a bit funny that way)
    
and to restore: 
    
    wmctrl -r L:C_N:titleBar_ID:system -e '0,0,0,600,30' 
    
### Много других рецептов 

* [K3](https://wiki.mobileread.com/wiki/K3_Index#Screensaver.2C_Font.2C_and_Layout_Hacks)
* [Kindle Touch Hacking](https://wiki.mobileread.com/wiki/Kindle_Touch_Hacking)
        
## Прочие ссылки

Горячие кнопки - в отличие от KUAL их надо помнить, зато наиболее
частые операции можно делать гораздо быстрее:
[lauchpad](https://www.mobileread.com/forums/showthread.php?t=97636)

[One more terminal emulator for kindle](https://www.mobileread.com/forums/showthread.php?t=154500)

[WebLaunch](https://www.mobileread.com/forums/showthread.php?t=210210), [GitHub](https://github.com/PaulFreund/WebLaunch).
Базируется на WebKit (`waf`) которого нет в kindle keyboard.