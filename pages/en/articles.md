---
layout: default
lang: en
ref: articles
permalink: /en/articles.html
---

<div class="panel-group">
<div class="panel panel-default">
<div class="panel-heading">{{ site.data.localization.history[page.lang] }}</div>
    <div class="panel-body">
        <table>
          {% for post in site.posts %}
            {% if page.lang == post.lang %}
                <tr>
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

