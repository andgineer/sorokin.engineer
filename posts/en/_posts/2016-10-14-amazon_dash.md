---
layout: post
lang: en
ref: amazon_dash
title: "Smart wifi button for Synology (amazon dash hack)"
comments: true
summary: ...amazon button (dash) hack...
tags: [osx, amazon button, dash, python, docker, synology]
---

![](/images/amazon_dash.png)

## TL; DR;
[Installation manual](http://masterandrey.com/posts/en/amazon_dash_install/)

## General

Place that button to wall, and event would be added into Google sheet or calendar,
or you can use [IFTTT Maker](https://ifttt.com/maker_webhooks).

Your children would like it and it helps to do something regularily.

And even for adults is easer to press button that to search for an app in your phone.

## Solution

In my opinion tha
[amazon dash](https://www.amazon.com/b/?ie=UTF8&node=10667898011)
is the cheapest and simplest solution.

They even sale the from time to time for $0.99.

But regular $5 is very-very cheap.
In China [aliexpress](https://www.aliexpress.com) you can buy ESP8266 for $2 or NodeMCU for $4, 
but also you would need case, button, batter, LED, couple of hours with soldering iron
and couple of hours to assemble and debug your firmware..

To buy Amazon button you need Amazon Prime subscription, but it's free first month
and after that this is only $10/month.

To do something usefull after button press you need some server application. 
My app [приложение](https://github.com/masterandrey/docker-amazon-dash/) works in 
[Docker container](https://hub.docker.com/r/masterandrey/amazon-dash/) 
and can run for example on [Synology](https://www.synology.com). 

In fact you can use it anywere where installed 
[docker](https://www.docker.com).

But in case of macOS and windows, docker runs inside virtual machine, so it cannot sniff
your network.

You can use my app **without** docker, but for that you should install [python3](https://www.python.org/downloads/) 
and libraries listed in
[pip.requirements.txt](https://github.com/masterandrey/docker-amazon-dash/blob/master/pip.requirements.txt)
and all system dependencies for them.
So I recommend to use docker, to not mess with this and to not change your system.

## Detail

Amazon button based on poweful ARM Cortex CPU, but now nowbody knos how to use it for
something more useful than flash LED.

So we use button in very simple way - look for any appearance of the button in network
and count each one as press.

My [application](https://github.com/masterandrey/docker-amazon-dash) to sniff
 network traffic use python library [scapy](https://github.com/phaethon/scapy).

There are a lot of other solutions for amazon button
but I could not find one already packed in docker and with event logic.

Button can register not just presses but event duration (for that you should press
at the beginnig and at the end).

[Installation manual](http://masterandrey.com/posts/en/amazon_dash_install/).
