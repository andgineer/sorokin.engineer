---
layout: post
lang: en
ref: amazon_dash_button_hack
title: "Smart wifi button and Docker on Synology (Amazon Dash Button hack)"
comments: true
summary: ...amazon dash button hack...
tags: [amazon dash button, python, docker, synology]
---

![](/images/amazon_dash.png)

## TL; DR;
[Installation manual](http://masterandrey.com/posts/en/amazon_dash_button_hack_install/)

## General

Place that button on wall, press it, and event would be added into Google Sheets 
or Google Calendar, or something would be done in [IFTTT](https://ifttt.com).

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

To buy Amazon button you need Amazon Prime subscription, but it's free first month
and after that this is only $10/month.

To catch button press and to do something usefull after press you need constantly running application. 
My [application](https://github.com/masterandrey/docker-amazon-dash-button-hack/) works in 
[Docker container](https://hub.docker.com/r/masterandrey/amazon-dash-button-hack/) 
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

Amazon button based on poweful ARM Cortex CPU, but a the moment nobody knows how to use it for
something more useful than flashing LED (and even that is very tricky).

So we do not hack Amazon Button actually but use it in very simple way - look for 
any appearance of the button in network and count each one as a press.

My [application](https://github.com/masterandrey/docker-amazon-dash-button-hack) sniffs
 network traffic using python library [scapy](https://github.com/phaethon/scapy).

There are a lot of other solutions for Amazon Dash Button hack
but I could not find one already packed in Docker and with event logic.
My Docker container is based on Alpine Linux and has very small size, it uses close to nothing
amount of your Synology resources.

With my app you can not only reqister just press but also event duration (for that you 
should press button at the beginning and at the end of the event).

[Installation manual](http://masterandrey.com/posts/en/amazon_dash_button_hack_button_install/).
