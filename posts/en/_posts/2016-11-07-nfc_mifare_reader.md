---
layout: post
lang: en
ref: nfc_mifare_reader
title: "Moscow subway NFC cards and MIFARE readers from ACS (ACR1281 и ACR122)"
comments: true
tags: [NFC, MIFARE, python]
redirect_from: "/posts/en/nfc_mifare_reader/"
---

![](/images/acr1281.jpg)

Here is my experience with [ACS](https://www.acs.com.hk) readers.
Hope that will save time if you have to use them.

I worked with readers [ACR1281](https://www.acs.com.hk/en/products/397/acr1281u-c2-card-uid-reader/)
and [ACR122](https://www.acs.com.hk/en/products/3/acr122u-usb-nfc-reader/).

Of cause you can use you NFC-enabled mobile phone but in my case I had to develop
Windows application for work with Moscow subway system cards.

### Python library

I used `pyscard` (module `smartcard`).
It uses [PC/SC интерфейс](https://ru.wikipedia.org/wiki/PC/SC), 
so you need just very basic driver to send PC/SC commands to USB.

#### Ubuntu Linux

    $ sudo apt-get install libacsccid1 pcscd pcsc-tools

After installation check:

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

##### If pcsc_scan does not see reader:

https://oneguyoneblog.com/2016/11/02/acr122u-nfc-usb-reader-linux-mint/

    sudo nano /etc/modprobe.d/blacklist.conf

Add these two lines to the end of the file:

    install nfc /bin/false
    install pn533 /bin/false

Install Ubuntu dependancy `libnfc`:

    http://nfc-tools.org/index.php?title=Libnfc
    https://debian.pkgs.org/9/debian-main-i386/libpcsclite-dev_1.8.20-1_i386.deb.html
    
And install Python package:

    sudo apt-get install swig libpcsclite-dev 
    sudo -H pip3 install pyscard

#### Windows

Install Python package:

    $ python -m pip install pyscard
    
#### Install swig

Probably you need [swig](http://www.swig.org/) to compile Python library.
You can find swig installer for Windows or use linux apt-get, as shown before.

### ACR1281 multi interfaces

ACR1281 has three interfaces, for each card type
(SAM, contact cards, contactless cards). You see them as three readers and the names
are different in different OS.

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
                raise Exception('Not found supported reader')
            # reader - to use
            
And after that `reader.createConnection().connect()`

Alternatively you can just wait for any reader that first read a card:

        from smartcard.CardType import AnyCardType

        def wait_for_card(timeout=0):
            # Wait for card with ATR NXP card ISO 14443 Part 3 PICC (бесконтактные)
            # (atr == reader.atr & mask, zeroes in mask filter out variative part, 
            # this part in atr equals zero)
            cardtype = ATRCardType(
                atr=toBytes('3B 80 80 01 80 4F 0C A0 00 00 03 06 03 00 00 00 00 00 00 00'),
                mask=toBytes('FF F0 FF FF FF FF FF FF FF FF FF FF FF FF F0 FF FF FF FF 00')
            )
            return CardRequest(timeout=timeout, cardType=cardtype)
            
To connect to that reader `wait_for_card().service.connection.connect()`.

And in any case you can send `APDU` command: `connection.transmit(APDU)`.
            
### Block reading in different readers

Both readers are from the same company but you have to use different parameters to read a block.
Block this is MIFARE read unit, 16 bytes.

To read block:
1. Save the read key in reader
1. Auth block by the key (reader sends the key to smart card and it answers if you
can read the block with the key)
1. Read the block

For ACR122 you have to save key in address 0, but for ACR1281 - in address `0x20`.

          def save_key_in_reader(key):
            KEY_STRUCTURE = 0  # volatile memory
            if self.reader_type == 'acr122':
                self.KEY_NUMBER = 0
            else:
                self.KEY_NUMBER = 0x20
                
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
               raise Exception('Error saving key: {:02x} {:02x}'.format(sw1, sw2))

