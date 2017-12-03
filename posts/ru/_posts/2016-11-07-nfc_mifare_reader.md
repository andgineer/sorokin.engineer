---
layout: post
lang: ru
ref: nfc_mifare_reader
title: "NFC карты московского метро и особенности ридеров MIFARE ACS (ACR1281 и ACR122)"
comments: true
tags: [NFC, MIFARE, python]
---

![](/images/athena.png){:.post-title}

Структура карт моксковсого метро защищена NDA, поэтому я не буду про нее рассказывать. 
Тем более что и так достаточно публикаций, подробно описывающих и устройство карт метро 
и даже как их самому записывать.

В моем случае я столкнулся с особенностью ридеров компании [ACS](https://www.acs.com.hk),
которые и хочу описать.
Надеюсь, что мой опыт съекономит кому-то время.

В моем распоряжении были ридеры [ACR1281](https://www.acs.com.hk/en/products/397/acr1281u-c2-card-uid-reader/)
и [ACR122](https://www.acs.com.hk/en/products/3/acr122u-usb-nfc-reader/).

Конечно, сейчас многие мобильные телефоны с таким же успехом могут и считывать и записывать
MIFARE карты, но мне были необходимы ридеры для создания инструментального приложения,
работающего с картами московского метро.

### Python библиотека

Я работал с ридерами через библиотеку `pyscard` (модуль в python называется `smartcard`).
Она использует для общения с ридером [PC/SC интерфейс](https://ru.wikipedia.org/wiki/PC/SC), 
что означает, что нам нужен минимальный драйвер, который передает команды в ридер через USB.

#### Ubuntu Linux

На Ubuntu достаточно установить следующие пакеты

    $ sudo apt-get install libacsccid1 pcscd pcsc-tools

После подключения ридера проверить возможность работы с ним:

    $ pcsc_scan
    PC/SC device scanner
    V 1.4.27 (c) 2001-2011, Ludovic Rousseau <ludovic.rousseau@free.fr>
    Compiled with PC/SC lite version: 1.8.14
    Using reader plug'n play mechanism
    Scanning present readers...
    0: ACS ACR1281 1S Dual Reader 00 00
    1: ACS ACR1281 1S Dual Reader 00 01
    2: ACS ACR1281 1S Dual Reader 00 02
    
    Thu Nov 16 12:49:20 2017
    Reader 0: ACS ACR1281 1S Dual Reader 00 00
      Card state: Card removed, 
    Reader 1: ACS ACR1281 1S Dual Reader 00 01
      Card state: Card removed, 
    Reader 2: ACS ACR1281 1S Dual Reader 00 02
      Card state: Card inserted, Unresponsive card, 

##### Если pcsc_scan не смог найти ридер, то

https://oneguyoneblog.com/2016/11/02/acr122u-nfc-usb-reader-linux-mint/

    sudo nano /etc/modprobe.d/blacklist.conf

Add these two lines to the end of the file:

    install nfc /bin/false
    install pn533 /bin/false

Для работы драйвера ридера в Ubuntu необходимо установить зависимость `libnfc`:

    http://nfc-tools.org/index.php?title=Libnfc
    https://debian.pkgs.org/9/debian-main-i386/libpcsclite-dev_1.8.20-1_i386.deb.html
    
Далее установить Python библиотеку:

    sudo apt-get install swig libpcsclite-dev 
    sudo -H pip3 install pyscard

#### Windows

Установить Python библиотеку:

    $ python -m pip install pyscard
    
#### Установка библиотеки swig

Скорее всего, для сборки python-библиотеки (выполняемой при ее установке через PIP) 
потребуется установить системную библиотеку [swig](http://www.swig.org/).
Для Windows есть инсталлятор, для linux можно использовать apt-get, как показно выше.

### Несколько интерфейсов ACR1281

У ридера ACR1281 есть три интерфейса, по одному на каждый тип поддерживаемых им карт 
(SAM, контактные карты, бесконтактные карты). Он представляется в системе как три ридера, 
причем их названия разнятся в разных операционных системах.

В итоге у меня получился такой код для выбора бесконтактного интерфейса

            from smartcard.System import readers
            
            for reader in readers():
                reader_name = str(reader)
                if 'ACR1281' in reader_name and (reader_name.endswith('01') or 'PICC' in reader_name):
                    self.reader_type = 'acr1281'
                    break
                if 'ACR122U' in reader_name:
                    self.reader_type = 'acr122'
                    break
            else:
                raise Exception('Не найден поддерживаемый ридер карт')
            # reader - выбранный ридер
            
Далее `reader.createConnection().connect()`

Альтернативный вариант - ждать, какой ридер первым считает карту:

        from smartcard.CardType import AnyCardType

        def wait_for_card(timeout=0):
            # Ожидаем карту с ATR NXP карт ISO 14443 Part 3 PICC (бесконтактные)
            # (atr == reader.atr & mask, т.е. нули в mask отфильтровывают вариативную часть, 
            # которую приравниваем в параметре atr равной нулю)
            cardtype = ATRCardType(
                atr=toBytes('3B 80 80 01 80 4F 0C A0 00 00 03 06 03 00 00 00 00 00 00 00'),
                mask=toBytes('FF F0 FF FF FF FF FF FF FF FF FF FF FF FF F0 FF FF FF FF 00')
            )
            return CardRequest(timeout=timeout, cardType=cardtype)
            
Для дальнейших действий надо соединиться с тем ридером, который считал карту:
`wait_for_card().service.connection.connect()`.

Для обоих вариантов далее обмениваемся командами `APDU` через `PC/SC`: 
`connection.transmit(APDU)`.
            
### Чтение блоков на разных ридерах

Как оказалось, не смотря на то что ридеры выпущены одной компанией, для них следует применять 
разные наборы команд при чтении блоков.
Блок это единица размещения данных на MIFARE, 16 байт.

Точнее, разные команды нужны при сохранении в ридере ключа чтения для последующей авторизации
блока этим ключом (получения разрешения читать блок).

Порядок действий такой:
1. Сохраняем ключ в ридере в ячейке с указанным нами номером
1. Авторизуем блок (ридер предъявляет ключ смарт-карте и она говорит, разрешает ли читать
указанный блок указанным ключом)
1. Собственно читаем блок

Как оказалось, для ридера ACR122 при сохранении ключа в ридере надо использовать 
параметр "номер ячейки ключа" равный нулю, а для ACR1281 - равный `0x20`.
Если если сделать наоборот, то ключ не сохранится, ридер выдаст ошибку `63 00`.

          def save_key_in_reader(key):
            KEY_STRUCTURE = 0  # volatile memory
            if self.reader_type == 'acr122':
                self.KEY_NUMBER = 0
            else:
                self.KEY_NUMBER = 0x20  # Это специальный номер ячейки для "сессионного ключа" 
                # используемого в случае volatile key memory (KEY_STRUCTURE=0)
                
            load_key_command = toBytes(
              'FF 82 {key_structure:02x} {key_number:02x} {key_length:02x} {key}'.format(
                key_structure=KEY_STRUCTURE,
                key_number=self.KEY_NUMBER,
                key_length=len(key),
                key=toHexString(key)
              )
            )
            
            result, sw1, sw2 = connection.transmit(load_key_command)
            if sw1 != 0x90:
               raise Exception('Ошибка сохранения ключа сектора в ридере {:02x} {:02x}'.format(sw1, sw2))

