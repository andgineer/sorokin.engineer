---
layout: post
lang: en
ref: python_async
title: "Non-sequential Python"
comments: true
tags: [Python asyncio threads fork]
redirect_from: "/posts/en/python_async/"
---
![](/images/wool-yarn.jpg){:style="float: right;margin-right: 7px;margin-top: 7px;"}

<style type="text/css">
  h2 {
    content: "";
    clear: both;
  }
</style>

## Introduction

Modern sotware dent hvas a lot of options to perform application logic
in non-sequential way.

But you have to understand which option is the best for the task at your hand.

I wrote this text to give you the information to choose.

## Why we need non-sequential code

### Massive IO (input/output)

We use computers with separate subsystems for fast (and expensive) and slow
(and cheap) memory - RAM ("memory") and disk (even SSD).

Also we mean 'network' when we speak about IO.

So suppose you wrote web-server and you can handle requests pretty fast but
after that you need to send responce by network and that will take 100x times
more.

And during processing for example you spent 1us to process and 1ms to wait for data
from DB.

The problem that when you wait for DB or network you do not serve other client
requests. And for sure you can serve them - you have plenty of CPU power
and even DB and CPU - they are more effective if you have a number of requests
in parallel.

Если в этот момент к вам придут другие клиенты, они только установят на уровне операционной системы TCP
соединения, и будут стоять в очереди, ждать, когда осободится ваш обработчик.
Который, в свою очередь, просто ждет завершения ввода-вывода операционной системой.

### Complex calculations

For example machine learning tasks need a lot of CPU power.

And here we have just opposite situation as described above.
We use all our CPU power and would like to use even more (for example second 
CPU on the machine) just to serve client request faster.

### Daemons

For example our web-server shows weather forecast.
And have to download new forecast each hour.

Downloading of new forecast is long procedure and we cannot stop serving
current requests. And we even do not need to dounload the new forecast
as fast as possible - we can do that slow but important thing do not
slow down client requests that we serve at the moment of downloading
new forecast.

## Non-sequential options

![](/images/process_seq.png){:style="margin-right: 7px; margin-top: 7px;"}
![](/images/process_par_multy.png){:style="float: right; clear: both; margin-right: 7px;margin-top: 7px;"}
![](/images/process_par.png){:style="float: right; margin-right: 7px;margin-top: 7px;"}

**1st picture** - sequential way.
Tasks are served sequentially, one at a time.
2nd task will wait for the end of 1st task.

**2nd picture** pseudo=parallel - we perfome tasks by small peaces. 
So we will serve small tasks faster.
And we will serve 2nd task faster than 1st. But of cause by the cost of slowing
down 1st task.

How to do that in practice?

Operating system do that by the help of CPU - it gives each process small
chunk of time.

Inside process we can for example use system call for that. When one
application 'green thread' do some system call we intercept it
and after calling system we give control to other application
'green thread'. And when it do system call do the same. And again ang again.
the is additional advantage that most system calls mean IO - application
'green thread'in any case have to wait system to do some IO (read file,
send packet to network etc). And we use this 'natural pause' to execute another
application 'green thread'''
 
**3rd picture** we use two CPU so we really execute in parallel.

## Python GIL

[CPython](https://en.wikipedia.org/wiki/CPython) 
in general cannot use multi-threading effectively due to 
Global Interpreter Lock (GIL).

GIL in Python exists just by historical reasons and because CPython
developers want to interpret existing huge Python code most
effectively.

To remove GIL you need to use some multi-threading mechanisms even for
single-thread code (because in gerenal you cannot tell if it's single- 
or multi-threaded). And that will slow down nearly all Python application.
too high cost (https://en.wikipedia.org/wiki/Global_interpreter_lock).

In fact Python IO libraries and C-code for example in NymPy unlock GIL
so multi-threading work good in code with a lot of IO or with written on C
libraries.

But there is no sense in multi-threading for just a Python code - you will get
even wosrt performance in comparison with single-thread (and too complicated
code as well).

BTW there are a number of other (not CPython) Python interpreters without
GIL
([Jython](https://en.wikipedia.org/wiki/Jython), 
[IronPython](https://en.wikipedia.org/wiki/IronPython)).
[PyPy fork](https://bitbucket.org/pypy/pypy/raw/stm-thread/pypy/doc/stm.rst).

## Ok with theory but how to do that in practice

Below are a number of way to have non-sequential Python code.

## Multi-processing

Just have running as many our application instances as we want.
And let the OS do all the dirty task in managing resources between this
processes.

Of cause you would not run hundreds of instances - too heavy memory
overhead and CPU resources waste due to switching between processed.

And all the instances are separate - they can communicate but this is not very
efficient.

Example of [multiprocessing](https://docs.python.org/3/library/multiprocessing.html)
usage:

{% highlight python %}
{% include src/multiprocessing.py %}
{% endhighlight %}
    hello alice
    hello bob
    alice done!
    bob done!

#### Properties
Let OS manage resources between our processes.

#### Pluses
* OS manage resourses very well (for a reasonable number of processes).
* Absolute isolation. Very simple logic (if you do not need inter-process
communications)
* No Python GIL.

#### Minuses
* High cost to fork and keep running separate OS processes.
* High memory consumption (each process has separate Python interpreter).
* High cost switching between processes (this is harware based but in any
case we need to do a lot of things).
* Bad choice if you need a lot of communication between your "application
threads". There are a number of very convenient tools in Python
multi-processing module but in any case this is expensive inter-communications.

#### Where to use
* We need to use all CPU for heavy computation - run at least as many
processes as number of CPU
* Effectively use wait for IO - just run a small number of processes
so when one whit others will work.
* Background work without a lot of communications with main application logic.
Run separate process for each backgroun task. Conside usage of appropriate
tool like [Celery](http://www.celeryproject.org).
    
## Multi-threading

Ancient way from our software engineering ancestors.

In python API is the same as for multi-processing.

{% highlight python %}
{% include src/multithread.py %}
{% endhighlight %}
    hello alice
    hello bob
    alice done!
    bob done!

#### Properties
As in multy-processing we delegate CPU sharing task to OS.
But now we have more fine-grade control.

#### Pluses
* The most efficient way to use all CPU. 
* A lot of knowlidge and documentation - this way is mostly reaserched
in many years of usage.

#### Minuses
* Launching thread is cheaper than launching process, but still pretty
expensive.
* The same about switching between threads.
* You cannot have thousands of threads. Ok you can if you want to but in
this case CPU mostly will work for inter-thread switching and will have
very litle time for useful work.
* Very complex in implementation. You have to read a lot and spend years in
practicing it before you fill confident and can write stable applications.
* Because of Python GIL this way good only for waiting for IO and for
non-python libraries.

#### Where to use
* Background tasks and waiting for IO.
* Small amount of parallel threads.
* Simple intre-thread communication if you do not wont spent in debugging
all your life.

## Green threads and asynio coroutines

Cooperative multi-tasking.

All `green threads` are executed in `execution loop` as `coroutines`.
`Execution loop` take `green threads/coroutines` one by one and execute them.

When `green thread/coroutine` stop execution to wait for IO or some
event, `execution loop` gets nest `green thread`.

All this works just because `green threads/coroutines` stops at some moments
by themself and gave control back to `execution loop` which start next
`green thread`. 
So this is "cooperative multi-threading" and works only if all `green threads`
are polite and gave control back to `execution loop` from time to time.

In fact `green threads` just old version of the same technic that now we call 
`asyncio`.

But now `asyncio` is official standard for Python and a lot of libraries use it.

###  Green threads

There are a number of implementations.
One example -[gevent](http://www.gevent.org/).

It uses `monkey patching`.
This is a way how to change system libraries so they will catch
control on all IO calls and call `execution loop`.

For example if we want `urllib` to use patched `socket` and cooperate
 with `execution loop`:

    from gevent import monkey
    monkey.patch_socket() 
    import urllib3

From this point `urllib` will send control to `execution loop` each time
somebody wait for network IO.

So just do `monkey patching` and after that you can use the patched library
just as usual.

{% highlight python %}
{% include src/greenlets.py %}
{% endhighlight %}
    hello alice
    hello bob
    bob done!
    alice done!
    
In this example we patched `time.sleep`. 
If you comment `monkey.patch_all()` then output will be different:

    hello bob
    hello alice
    bob done!
    alice done!

In fact there is special `gevent.sleep` in `gevent` so no need in
 patching`time`. 
But my intension was to demonstrate the technic. Also you can see how is this
implicite and had to see. Looking at the code you have no idea that in fact
it can stop execution and execute another code.

#### Pluses
* Не надо существенно раскрашивать `async/await`, как в `asyncio`, код зеленого потока.
* Дешевое переключение между потоками.
* Потоков может быть много.
* Накладные расходы невысоки.

#### Minuses
* `Monkey patching` неочевиден, поэтому даже при большом опыте вы будете очень приближенно понимать, 
что происходит в приложении. И оптимизация работы станет увлекательным научным приключением.

#### Where to use
Можно попробовать применить для большого объема унаследованного кода, который не предполагал 
асинхронность.

Есть риск надолго завязнуть в сложной отладке и так и не получить реально несинхронного выполнения,
но зато при успехе экономим время на переписывании старого кода. 


### Asyncio

Стандарт для Python.
Имеет специальные ключевые слова в языке. 

{% highlight python %}
{% include src/async.py %}
{% endhighlight %}
    hello alice
    hello bob
    bob done!
    alice done!

#### Pluses
* В полном соответствии с Python принципами "явное лучше неявного" - полная прозрачность 
происходящего, упрощающая дальнейшее сопровождение приложений.
* Дешевое переключение между потоками.
* Потоков может быть много.
* Накладные расходы невысоки.
* В сочетании с отсутствие `monkey patching` получаем достаточно простое логически решение.
Которое на порядок проще писать и отлаживать, чем multy threading. 

#### Minuses
Надо существенно изменять исходные код.
После чего его использование в синхронном режиме, хотя и вполне возможно, но уже довольгно громоздко
и менее эффективно (придется все равно стартовать цикл обработки).

#### Where to use
Не стоит использовать `asyncio`, если у используемых вами библиотек ввода/вывода нет 
`asycnio` вариантов. Такие варианты сейчас появились почти для всего, но если вам не уйти от 
использования не поддерживаемой библиотеки, для которой никому не понадобилось делать `asyncio` вариант,
возможно, рациональнее для начала попробовать сделать `monkey patching`, чем тратить много усилий на
создание `asyncio` версии своими силами. 

В новом коде рекомендуется использовать именно `asyncio`.
Вполне решаемо совмещение `зеленых потоков` и `asyncio` - тем или иным образом надо решить
вопрос использования единого `цикла выполнени` для обеих библиотек.


## Call-back hell

Для полноты упомяну js-way.
Мы можем при вызове ввода-вывода указывать функции, которые после ввода-вывода надо будет вызвать.
И после этого продолжать выполнение нашей программы.

Очевидно, что при этом приложение становится конечным автоматом.
Вы пишете не последовательный код выполнения программы, а море обработчиков всевозможных событий.
Которые, зачастую, логически совсем не выглядят событием (скажем, завершение открытия файла).

В принципе, несложный интерфейс пользователя так можно реализовать.
Но как только нам надо сделать сложную обработку, мы получим очень запутанное приложение.

Поскольку `callback` это про способ взаимодействия с `coroutines`, чтобы его продемонстрировать я 
взял `asyncio`.

Пример получился не страшным. Чтобы понять, во что в итоге выльется такой дизайн, вам надо далее
представить, что после получения результатов от `bob` и `alice` вам надо далее что-то с ними сделать.
Но вы уже не можете это описать как последователность инструкций - вам надо в обработчике `on_result`
понять, что все нужные результаты уже получены и далее куда-то передать управление. А там будет 
очередной разрыв процесса выполнения, когда вам потребуется ждать другие `coroutines`. И порой это 
будет вложенным процессом. В итоге приложение будет состоять из большого числа сложно связанных
функций, и из кода будет трудно понять последовательность их выполнения.

{% highlight python %}
{% include src/callback.py %}
{% endhighlight %}
    hello alice
    hello bob
    bob done!
    alice done!
    
## libuv and others

В описанном выше я не упоминал, как именно `цикл выполнения` понимает, что операционная система,
например, закончила считывание файла, и, значит, управление можно опять давать той `coroutine` что
этого ожидала.

Конкретные реализации не только существенно зависят от операционных систем.
В рамках каждой операционной системы может быть несколько способов этого сделать.

Поэтому имеется несколько вариантов реализации `цикла выполнения`.
Понять, какой из них лучше, и для чего - нетривиальное исследование.
Сложность связана с тем, что эффективность надо измерять в реальных условиях.
А реальный ввод-вывод очень сложно сделать повторяемым.
При этом его задержки должны быть достаточно существенными, чтобы продемонстривать
эффективность или неэффективность. На фоне этих задержек не просто поймать вклад
в производительность собственно `цикла выполнения`.

### Slide show
* [PDF](/files/PythonAsync.pdf)
* [PowerPoint](/files/PythonAsync.pptx)