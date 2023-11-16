---
layout: post
lang: en
ref: itunes_audiobook_from_mp3
title: "iTunes (iPhone) Audiobook from mp3"
comments: true
tags: [ios, audiobook, python]
redirect_from: "/posts/en/itunes_audiobook_from_mp3/"
---
![](/images/brothers_karamazov_ardis.jpg)

## iTunes Audiobooks from MP3 Files with Incorrect Tags
You have tried to upload audiobook files to iTunes or some other player and noticed
that all the MP3 tags have turned into gibberish, and the playback order has become completely random. 
Now the book might start with the epilogue, for example.

This issue is not specific to where you obtained the audiobook files. It happens to me with both online purchases and ancient CD discs.

## How to Fix It

Install [audiobook-tags](https://github.com/andgineer/itunes-audiobook-from-mp3)

### Installation
Install using [`pipx`](https://pypa.github.io/pipx/) for isolated environments, which prevents interference
with your system's Python packages.

Once `pipx` is set up:

    pipx install audiobook-tags

### Fix the tags

To convert audio files tags, for example, in the directory `~/Downloads/audiobook`:

    audiobook-tags ~/Downloads/audiobook -n=name

This command will fix the tag encoding, assuming it's Win1251 (if you need a different encoding, use the `--encoding` argument). 

It will also sort the order based on the file name. 

If you need a different order, refer to the description of the `--num` argument.

By default it is looking for `mp3`, you can change that with the `--suffix` argument, for example `-s="m4b"`.

If you want to try it without changes to files, add `--dry` argument.

To get help on the program, use:

        audiobook-tags --help

That's it! You can now upload the files to a player like [audible](http://www.audible.com) or any other and start listening.

For example, I personally like the player [evermusic](https://apps.apple.com/ru/app/evermusic-%D0%BE%D1%84%D1%84%D0%BB%D0%B0%D0%B9%D0%BD-%D0%B0%D1%83%D0%B4%D0%B8%D0%BE%D0%BF%D0%BB%D0%B5%D0%B5%D1%80/id885367198)
which seems to be available for Android as well.

## Creating an Audiobook in iTunes

If you want to create an audiobook in iTunes, there is an additional step after importing the files.

Select the audiobook files and go to their properties:

![](/images/itunes_media_kind.png)

Specify that it's an audiobook there:

![](/images/itunes_media_kind_select.png)

Then it will be moved to the audiobook section.
