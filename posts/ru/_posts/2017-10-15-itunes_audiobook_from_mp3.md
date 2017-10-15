---
layout: post
lang: ru
ref: itunes_audiobook_from_mp3
title: "Аудиокниги iPhone из кривых mp3"
comments: true
tags: [iOS, audiobook, python]
---
![](/images/brothers_karamazov_ardis.jpg)

## Аудиокниги iTunes из кривых mp3
... или чем заняться после утренней пробежки, но перед завтраком...

Одним прекрасным, привычно дождливым питерским утром, я решил немного побегать в парке.

Одел кроссовки, но когда хотел запустить для компании аудиокнигу из кривейшего приложения Слушай!
созданного litres, оно мне сказало "я вот вижу, что ты невнимательно слушал, так что давай
послушаем ее опять с начала". В книге почти 200 файлов и 51 час аудио. Я как-то был не готов,
стоя в коридоре в кроссовках, искать, где я остановился, поэтому я запустил в любимой 
[ЯМузыке](https://music.yandex.ru/home) подборку для бега (у меня это в основном клубная 
танцевальная музыка). 

А вернувшись, попробовал загрузить купленные мной у литреса аудиокниги в какой-то менее проблемный плеер.
Например [audible](http://www.audible.com), в котором я прослушал сотни книг, и он ни разу меня не подвел.

Получился жесткий облом - ладно что все mp3 тэги были кракозябрами, мне же слушать, а не смотреть.
Но порядок, который в книге определялся только порядком файлов (а тег номера трека почему-то отсутствовал
в mp3 тэгах), iTunes творчески переработал в порядок по именам файлов, так что теперь книга начиналась с 
эпилога.

Беглый поиск ничего не дал - на [4pda](https://4pda.ru/forum/index.php?showtopic=114851) 
ремондовали либо какой-то софт для windows (windows работает у меня
в parallels но нет желания лишний раз ковыряться в windows софте), или платные приложения для MacOS,
которые к тому же никак не решали проблему кодировок, хотя и верно расставляли поярдок файлов.

В итоге я взял Python3, [eyeD3](https://eyed3.readthedocs.io/en/latest/) и написал вот такую утилитку
[Python app](https://github.com/masterandrey/itunes-audiobook-from-mp3).

Поставить программно все нужные свойства не удается - похоже, что передвинуть в аудиокниги можно 
только в самом iTunes.

После импорта файлов выберите в свойствах
![](/images/itunes_media_kind_select.png)
и укажите там, что это аудиокнига:
![](/images/itunes_media_kind_select.png)
тогда она переметится в раздел аудиокниг.




