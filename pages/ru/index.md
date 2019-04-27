---
layout: default
lang: ru
ref: blog
permalink: /ru/index.html
---

<div class="panel-group">
<div class="panel panel-default">
<div class="panel-heading">{{ site.data.localization.history[page.lang] }}</div>
    <div class="panel-body">
        <table>
          {% for post in site.posts %}
            {% if page.lang == post.lang %}
                <tr>
                    <td>{{ post.date | date: "%Y.%m.%d" }}</td>
                    <td>
                        <a href="{{ post.url }}">{{ post.title }}</a>
                    </td>
                </tr>
            {% endif %}
          {% endfor %}
        </table>
    </div>
</div>
</div>
