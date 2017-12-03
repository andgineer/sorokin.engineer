---
layout: post
lang: ru
ref: nfc_mifare_reader
title: "NFC карты московского метро и особенности ридеров MIFARE ACS (ACR1281 и ACR122)"
comments: true
tags: [NFC, MIFARE, python]
---

![](/images/athena.png){:.post-title}

Структура карт метро защищена NDA, поэтому я не буду про нее рассказывать. 
Тем более что и так достаточно публикаций, подробно описывающих и устройство карт метро 
и даже - как их самому записывать.

В моем случае я столкнулся с особенностью ридеров компании [ACS](https://www.acs.com.hk),
который и хочу описать.
Надеюсь, что мой опыт съекономит кому-то время.

В моем распоряжении были ридеры [ACR1281](https://www.acs.com.hk/en/products/397/acr1281u-c2-card-uid-reader/)
и [ACR122](https://www.acs.com.hk/en/products/3/acr122u-usb-nfc-reader/).

### Python библиотека

Я работал с ридерами через библиотеку pyscard (модуль в python называется smartcard).
Она использует для общения с ридером [PC/SC](https://ru.wikipedia.org/wiki/PC/SC) интерфейс, 
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

Читаем здесь: https://oneguyoneblog.com/2016/11/02/acr122u-nfc-usb-reader-linux-mint/

    sudo nano /etc/modprobe.d/blacklist.conf

Add these two lines to the end of the file:

    install nfc /bin/false
    install pn533 /bin/false

Для работы драйвера ридера в Ubuntu необходимо установить зависимость `libnfc`:

    http://nfc-tools.org/index.php?title=Libnfc
    https://debian.pkgs.org/9/debian-main-i386/libpcsclite-dev_1.8.20-1_i386.deb.html
    
Далее установить Python библиотеку:

    $ sudo apt-get install swig libpcsclite-dev 
    $ sudo -H pip3 install pyscard

#### Windows

Установить любой pc/sc драйвер.
Далее установить Python библиотеку:

    $ python -m pip install pyscard
    
#### Установка библиотеки swig

Скорее всего, для сборки python-библиотеки (выполняемой при ее установке через PIP) 
потребуется установить системную библиотеку [swig](http://www.swig.org/).

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
            
### Чтение блоков на разных ридерах

Как оказалось, не смотря на то что ридеры выпущены одной компанией, для них следует применять 
разные наборы команд при чтении блоков (единицы размещения данных на MIFARE,
16 байт).
Точнее, при авторизации блока ключом для чтения.
Ключ для чтения надо "сохранить в ридере", чтобы далее "авторизовать" им блок.

Как оказалось, для ридера ACR122 при таком сохранении ключа в ридере надо использовать 
параметр "номер ключа" равный нулю, а для ACR1281 - равный  `0x20`, и никак иначе - если
есделать наоборот, то ключ не сохранится, ридер выдаст ошибку.

            KEY_STRUCTURE = 0  # volatile memory
            if self.reader_type == 'acr122':
                self.KEY_NUMBER = 0
            else:
                self.KEY_NUMBER = 0x20  # Это специальный номер для "сессионного ключа" используемого в 
                # случае volatile key memory (KEY_STRUCTURE=0)
                
            load_key_command = toBytes(
              'FF 82 {key_structure:02x} {key_number:02x} {key_length:02x} {key}'.format(
                key_structure=KEY_STRUCTURE,
                key_number=self.KEY_NUMBER,
                key_length=len(key),
                key=toHexString(key)
              )
            )

