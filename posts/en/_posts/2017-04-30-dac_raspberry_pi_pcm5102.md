---
layout: post
lang: en
ref: raspberry-dac
title: "Internet radio: How to connect I2S DAC to raspberry pi"
comments: true
tags: [raspberry pi, DAC, HAT, PCM5102]
---

To build your DIY internet radio, you can connect raspberry pi to some DAC
(digital - analog converter) and add any audio speakers with amplifier.
And use the music player you like ([volumio](https://volumio.org/),
rune audio, max2play etc).
You control this players from your phone, so no need in any knobs on the intenet
radio box, you can hide it somewhere.

You need DAC because raspberry pi has very-very poor sound from integrated on it
3.5mm headphones jack.

## Alternative if you do not want to mess with I2S DAC
You can use any HDMI-Video/audio adapter (search on [aliexpress](https://www.aliexpress.com) for
 "hdmi rca".
This is a small box with HDMI input and RCA output (yellow for video, red and white
for audio).
With HDMI cable this is the same money as I2S DAC.

## I2S DAC PCM5102 on aliexpress
Search on [aliexpress](https://www.aliexpress.com) for "Raspberry Pi PCM5102".

Of cause you can buy [HiFiBerry](https://www.hifiberry.com/) for $35.
But aliexpress models four(!) times cheaper and based on the very same IC.

| RCA | 3.5mm headphones jack |
| ![](/images/PCM5102-DAC-Decoder-I2S-Player.jpg) &nbsp;&nbsp;| ![](/images/Sound-Card-I2S-PCM5102.jpg) |


Sellers claim that this is Raspberry Pi HAT extensions, but that is not true.
You can connect them to HAT socket on Raspberry Pi, but you need some wiring,
you cannot just insert them as HiFiBerry.

## Raspberry Pi A/B
On the very-very old raspberry pi the pins that you need to connect I2S DAC are somethere on
the board, not in any socket.
I do not think that you have such a board so below I describe more modern ones.

Raspbery Pi before "+" version have the pins on 8-pins `P5` socket, which is below main
HAT 26-pins socket `P1`.

In many cases you have to solder `P5` for yourself:
[video from HiFiBerry](https://www.hifiberry.com/solder-the-p5-header-to-your-raspberry-pi-model-ab/).

Take into account that it is supposed to be soldered from back of the board (on the video above
they solder it from front).
So odd/even pins in `P5` is opposite as in `P1`.
You can check youself - on `P5-1` should be 5v, on `P5-2`
3.3v (and last pins of `P5`, `P5-7` & `P5-8` is ground).

## Raspberry Pi A\+/B\+, Raspberry Pi 2, Raspberry Pi 3

On Raspberry Pi+, Raspberry Pi 2 & Raspberry Pi 3
all needed pins are in main 40-pins HAT socket.
It's name now `J8` and it consists of all 25 pins from old `P1`, and additional pins.

![](/images/raspberry-pi-p5.png)

## How to connect I2S DAC to Raspberry Pi

### 1st DAC version (with fewer pins):

| **DAC** | **Pi A/B** &nbsp;| **Pi A\+/B\+, Pi2, Pi3** |
|-----|-----|-----|
| Vcc (+5v) | P5-1 | J8-2 |
| +3.3v (not used, just to check youself) &nbsp; | P5-2 | J8-1 |
| BCK | P5-3 | J8-12 |
| LRCK | P5-4 | J8-35 |
| DATA | P5-6 | J8-40 |
| Gnd | P5-7 | J8-39 |

In the board description seller wrote that BCK & DATA marked inverse.
But in fact I connected as marked (BCK is the last pin in DAC's socket) and everything works fine.

### 2nd DAC:

Connect additional pins as:

| **DAC** | **Pi A/B** &nbsp;| **Pi A\+/B\+, Pi2, Pi3** |
|-----|-----|-----|
| GND |	P1-6 | J8-6 |
| FLT (gnd) | P1-14 | J8-14 |
| DMP (gnd) | P5-8 | J8-20 |
| SCL	| P1-5 | J8-5 |
| FMT (gnd) | P1-18 | J8-18 |
| XMT (3.3v) &nbsp; | P1-1 | J8-1 |


## How to setup I2S DAC in Volumio

* Open volumio web-interface - if you have only one volumio you can use [http://volumio.local](http://volumio.local)
* Press on cog on top right corner of volumio window
* Select `Playback` menu item
* Switch on I2S DAC and for I2S driver select `Generic I2S DAC`
* Press `Apply`
* Volumio ask to reboot raspberry pi - answer yes
