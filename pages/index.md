---
layout: default
lang: en
ref: blog
permalink: /index.html
---

<div class="posts">
  {% assign posts=site.posts | where:"lang",page.lang %}
  {% for post in posts %}
    <article class="post">

      <h1><a href="{{ site.baseurl }}{{ post.url }}">{{ post.title }}</a></h1>

      <a href="{{ site.baseurl }}{{ post.url }}" class="read-more">Read More</a>
    </article>
  {% endfor %}
</div>