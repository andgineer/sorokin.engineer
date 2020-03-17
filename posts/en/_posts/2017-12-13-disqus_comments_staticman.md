---
layout: post
lang: en
ref: staticman
title: "Disqus comments alternative: github issues (Staticman)"
comments: true
tags: [github pages]
redirect_from: "/posts/en/disqus_comments_staticman/"
---

![](/images/staticman.png){:style="float: right;margin-right: 7px;margin-top: 7px;"}

<style type="text/css">
  h2 {
    content: "";
    clear: both;
  }
</style>

## Exodus

After news about disqus, I decided to move comment system of my blog to github review.
Because my site is static and live on github itself.

Downside from this solution - no spam protection and no engine to control comments
by users, because all comment now posted by bot.

I used [Staticman](https://staticman.net/docs/).

So you just give hitm contributor rights in your github repository with your blog
and add [config](https://github.com/andgineer/sorokin.engineer/blob/master/staticman.yml)
into root of your repository.

Example of [html](https://github.com/andgineer/sorokin.engineer/blob/master/_includes/staticman.html) with comments list and comment post form.
