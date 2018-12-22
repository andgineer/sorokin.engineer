---
layout: post
lang: ru
ref: staticman
title: "Замена комментариев disqus на комментарии github"
comments: true
tags: [github pages]
redirect_from: "/posts/ru/disqus_comments_staticman/"
---

![](/images/staticman.png){:style="float: right;margin-right: 7px;margin-top: 7px;"}

<style type="text/css">
  h2 {
    content: "";
    clear: both;
  }
</style>

## Исход

После новостей о рекламе в disqus, я решил перевести блог на комментарии в самом gihub
на котором и живет блог.

Решение весьма спорное, в основном потому что нет никакой защиты от спама, но пока
я неуловимы Джо можно этим не заморачиваться, а потом посмотрим.

Ну и второй существенный минус - никакого механизма управления комментариями со стороны пользователей, поскольку в github они попадают от имени бота.

Использованный мной бот [Staticman](https://staticman.net/docs/) не мой.

Чтобы он заработал надо дать ему праава, как описано в его доке, добавить его [конфиг](https://github.com/masterandrey/masterandrey.com/blob/master/staticman.yml)
в  корень вашего github репозитория с блогом.

Ну и написать [html](https://github.com/masterandrey/masterandrey.com/blob/master/_includes/staticman.html) с формой и списком комментариев.
