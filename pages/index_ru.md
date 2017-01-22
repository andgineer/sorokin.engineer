---
layout: default
lang: ru
ref: blog
permalink: /index_ru.html
---

<div class="container-fluid">
  <ul class="list-group">
  {% assign posts=site.posts | where:"lang",page.lang %}
  {% for post in posts %}
    <article class="post">

      <li class="list-group-item borderless">
        <a href="{{ site.baseurl }}{{ post.url }}">{{ post.title }}</a>
      </li>

    </article>
  {% endfor %}
  </ul>
</div>