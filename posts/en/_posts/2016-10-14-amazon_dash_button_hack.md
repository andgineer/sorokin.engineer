---
layout: post
lang: en
ref: amazon_dash_button_hack
title: "Amazon Dash Button hack: Your DIY smart wifi button"
comments: true
tags: [amazon dash button, python, docker, synology]
---

![](/images/amazon_dash.png)

## TL; DR;
[Installation manual](http://masterandrey.com/posts/en/amazon_dash_button_hack_install/)

## General

Place that button on wall, press it, and event would be added into Google Sheets 
or Google Calendar, or something would be done in [IFTTT](https://ifttt.com).

Events you can visualize by thousands ways, 
[for example](http://masterandrey.com/posts/en/iot_calendar_synology/).

Your children would like it and it helps to keep doing something regularily.

And even for adults it is easier to press button than to search for an app in your 
smartphone.

## Solution

In my opinion the
[Amazon Dash Button](https://www.amazon.com/b/?ie=UTF8&node=10667898011)
is the cheapest and simplest solution.

They even sale them from time to time for $0.99.

And regular $5 is very cheap.
In Chinese [aliexpress](https://www.aliexpress.com) you can buy ESP8266 for $2 or NodeMCU for $4, 
but also you would need case, button, battery, LED, couple of hours with soldering iron
and couple of hours to assemble and debug your firmware..

If we are speaking about other buttons that do not require soldering (like Amazon Dash Button):

| [AWS IoT Button](https://aws.amazon.com/iotbutton/) | $20 | 
| [flic](https://flic.io/store/) | $35 |
| [particle.io button](https://store.particle.io/#internet-button) | $50 |
| [XiaoMi Aqara Smart Wireless Switch Key](https://www.aliexpress.com/wholesale?catId=0&initiative_id=SB_20180105060003&SearchText=XiaoMi+Aqara+Smart+Wireless+Switch+Key) | $8 per buton (switch) and $25 one Zigbee hub (gateway) |
{:.unstripedtable}

<br>
You just cannot compare that with $5 (moreother with $0.99).

To buy Amazon button you need Amazon Prime subscription, but it's free first month
and after that this is only $10/month.

To catch button press and to do something usefull after press you need constantly running application. 
My [application](https://github.com/masterandrey/docker-amazon-dash-button-hack/) works in 
[Docker container](https://hub.docker.com/r/masterandrey/docker-amazon-dash-button-hack/) 
and can run for example on [Synology](https://www.synology.com). 

In fact you can use it anywere where installed 
[Docker](https://www.docker.com).

Remember that in case of OSX and Windows, Docker runs inside virtual machine, so it cannot sniff
your network.

You can use my app **without** docker, but for that you should install 
[python3](https://www.python.org/downloads/) and libraries listed in
[pip.requirements.txt](https://github.com/masterandrey/docker-amazon-dash-button-hack/blob/master/pip.requirements.txt)
and all system dependencies for them.
So I recommend to use Docker, to save your time and don't mess with your operating system libraries.

## Detail

Amazon button based on poweful CPU (ARM Cortex-M3 STM32 in old versions of buttons,
[Atmel ATSAMG55J19](http://www.atmel.com/images/atmel-11289-32-bit-cortex-m4-microcontroller-sam-g55_summary-datasheet.pdf) 
in late 2016 ones), but a the moment nobody knows how to use it for
something more useful than flashing LED (and even that is 
[very tricky](http://key-basher.blogspot.ru/2016/09/amazon-dash-button-version-2.html)).

So we do not hack Amazon Button actually but use it in very simple way - look for 
any appearance of the button in network and count each one as a press.

The button after press will flash red light because it is not configured to buy something.
But it will do the job all the same.

My [application](https://github.com/masterandrey/docker-amazon-dash-button-hack) sniffs
 network traffic using python library [scapy](https://github.com/phaethon/scapy).
 
It works with old Amazon Dash Buttons (before late 2016) and with 
[new Amazon Dash Buttons](https://mpetroff.net/2016/07/new-amazon-dash-button-teardown-jk29lp/).

There are a lot of other solutions for Amazon Dash Button hack
but I could not find one already packed in Docker and with event logic.
My Docker container is based on Alpine Linux and has very small size, it uses close to nothing
amount of your Synology resources.

For old buttons (before end of 2016) you could fake amazon server address and
call your script from the button, and even have nice green flash when pressed, but new buttons
require amazon SSL-sertificate on server side and this hack does not work.

With my app you can not only reqister just press but also event duration (for that you 
should press button at the beginning and at the end of the event).

[Installation manual](http://masterandrey.com/posts/en/amazon_dash_button_hack_install/).
