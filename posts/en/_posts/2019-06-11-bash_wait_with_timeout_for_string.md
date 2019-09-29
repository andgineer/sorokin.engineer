---
layout: post
lang: en
ref: bash_wait_with_timeout_for_string
title: "BASH tricks: how to wait with timeout for string from process"
comments: true
tags: [bash, perl]
---
![](/images/bash_timeout.png)

## How to wait for specific string from application with timeout

Suppose you have to run some application and wait for some string that means that 
everything is OKey. 

After that you want to kill the application.
And return success exit code (for example for you CI, for make etc).

And if there is no such string we want wait for some time and after that 
kill the application and return error exit code.

Well you are in luck - I can show you how to do that.

In any case this example will teach you some new tricks for you BASH Kung-Fu.

<script src="https://gist.github.com/andgineer/2555ba583bc675bf63e0fa399c627851.js"></script>

In first line you use Linux command timeout that will run process that you
specify in the parameter. And kill if after specified timeout.

Also I add parameter `-k` - so `timeout` will hard-kill the process if it won't terminate
gracefuly.

As test process I wrote Perl one-liner, it print some string, sleep for a moment and 
print another line.

And the main trick in last line.

Of cause we could use just grep. Easy.

But grep print only matches. But we want to see all the output.

So another Perl one-liner (this is exactly the best usage of Perl - do not write big 
programs in Perl if you want to stay sane).

It wait for the string and exit after that with success exit code.
If we did not find the string but Linux pipe already closed (that means the first 
process finished) it will return error exit code.

## How to brew install timeout in MacOS

There is no `terminate` on your initial installation of MacOS.

So you have to install [coreutils](https://formulae.brew.sh/formula/coreutils).

Just remember that all the names will be with `g` prefix, like `gtimeout`.
If you want tha same names as in Linux you have to modify `PATH` in your `~/.bashrc`.
Please read how on the same homebrew page.
