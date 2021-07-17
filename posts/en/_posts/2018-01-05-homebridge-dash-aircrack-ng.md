---
layout: post
lang: en
ref: airdump
title: "Fast reaction from Amazon Dash by aircrack"
comments: true
tags: [macos, amazon dash button]
redirect_from: "/posts/ru/homebridge-dash-aircrack-ng/"
---

![](/images/)

Using hack [AirCrack-ng](https://www.aircrack-ng.org) you will make your
Amazon Dash work faster.

### Ubuntu Linux install

    sudo apt-get install aircrack-ng
    
### MacOS install

    brew install aircrack-ng
    PATH=${PATH}:/usr/local/sbin
    airodump-ng-oui-update
    
### Python package

    sudo -H pip3 install pyrcrack

### Check

    import pyrcrack.management
    with pyrcrack.management.Airmon('wlan0') as f:
      print(f.interface)