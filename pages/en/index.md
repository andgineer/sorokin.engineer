---
layout: default
lang: en
ref: blog
permalink: /en/index.html
---

<div>
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