---
layout: post
lang: ru
ref: django_htmx_infinite_scroll
title: "Django реализация бесконечного списка на HTMX"
comments: true
tags: [Python, HTMX, Django]
---

![](/images/python-scroll.png){:.post-title}

Я расскажу как сделать бесконечный, динамически подгружаемый список на Django и HTMX.
Ни единой строчки JavaScript, ни единого CSS.

Я также подключил Bootstrap для стилизации, но это не обязательно.

## TL;DR
    git clone https://github.com/andgineer/django-htmx-infinite-scroll.git
    cd django-htmx-infinite-scroll
    . ./activate  # обратите внимание на точку в начале команды
    make init-db
    make run

Теперь откройте в браузере http://localhost:8000/ наш бесконечный список, который загружает очередные страницы 
по мере прокрутки.

## Как вам создать такое прилодение за пять минут

#### Создайте приложение Django
У вас должен быть установлен Python и pip.
Установим Django и создадим проект `core`  и приложение `django_htmx_infinite_scroll`:

{% highlight bash %}
pip install django faker
django-admin startproject core .
python manage.py startapp django_htmx_infinite_scroll
{% endhighlight %}

Добавим приложение в `INSTALLED_APPS` в `core/settings.py`:

{% highlight python %}
INSTALLED_APPS = [
    ...
    'django_htmx_infinite_scroll',
]
{% endhighlight %}

#### Создадим модель
Создадим модель в `django_htmx_infinite_scroll/models.py` подобную [BookPage](https://github.com/andgineer/django-htmx-infinite-scroll/blob/84d91ed61b86eb8c7c315ac4ab14b91f9a9101fe/django_htmx_infinite_scroll/models.py#L5)

Теперь Django знает о нашей модели и может создать таблицу в базе данных:

{% highlight bash %}
python manage.py makemigrations
python manage.py migrate
{% endhighlight %}

#### Наполним базу данных
Для тестирования создадим записи в базе данных. Для этого нам потребуется команда Django - добавьте содержимое
[add-pages.py](https://github.com/andgineer/django-htmx-infinite-scroll/blob/84d91ed61b86eb8c7c315ac4ab14b91f9a9101fe/django_htmx_infinite_scroll/management/commands/add-pages.py#L1)
в файл `django_htmx_infinite_scroll/management/commands/add-pages.py`.

Тепере можно вызвать `python manage.py add-pages`.

#### Создадим представление
Опишем два представления в `django_htmx_infinite_scroll/views.py`, их можно скопировать из
[views.py](https://github.com/andgineer/django-htmx-infinite-scroll/blob/84d91ed61b86eb8c7c315ac4ab14b91f9a9101fe/django_htmx_infinite_scroll/views.py#L1).

#### Добавим URL
Чтобы эти представления можно было вызвать, нам нужно добавить URL.

Добавим в `core/urls.py` ссылку на URL приложения:

{% highlight python %}
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("django_htmx_infinite_scroll.urls")),
]
{% endhighlight %}

И создадим `django_htmx_infinite_scroll/urls.py`:

{% highlight python %}
from django.urls import path
from . import views

urlpatterns = [
    path("", views.book, name="book"),
    path("book-page", views.book_page, name="book-page"),
]
{% endhighlight %}

Первый URL будет вызывать представление `book`, которое будет отображать страницы книги.
А второй будет выдавать страницы книги как для изначального отображения первых страниц, так и 
для загрузки очередной страницы книги из HTMX по мере прокрутки страницы браузера.

#### Создадим шаблоны
Мы почти закончили.
Осталось создать шаблоны для наших представлений.

Мы сделаем иерархию шаблонов, чтобы не дублировать код.

В каталог `django_htmx_infinite_scroll/templates` скопируйте файлы из
[templates/](https://github.com/andgineer/django-htmx-infinite-scroll/tree/main/django_htmx_infinite_scroll/templates).

#### Запустим сервер
Теперь можно запустить сервер и посмотреть на результат:

{% highlight bash %}
python manage.py runserver
{% endhighlight %}

Откройте в браузере http://localhost:8000/ и вы увидите прокручиваемый список страниц.

## Объяснение кода
#### HTMX бесконечная прокрутка
{% highlight python %}
{% raw %}
<div class="row justify-content-center"
        hx-get="{% url 'book-page' %}?page-number={{ page.number|add:1 }}"
        hx-swap="afterend"
        hx-trigger="revealed"
    <div id="page-{{ page.number }}" class="col-10">
        <h2 class="card-title text-center">{{ page.number }}</h2>
        <p class="card-text">{{ page.content }}</p>
    </div>
</div>
{% endraw %}
{% endhighlight %}

Чтобы показать одну страницу, мы используем код выше.

Он включает атрибут `hx-get` для указания URL AJAX-запроса.
Это вызывает наше представление `book_page` с номером страницы в качестве параметра.

Атрибут `hx-swap` определяет, куда должен быть вставлен ответ. `afterend` означает, что ответ будет
вставлен после текущего элемента.

Атрибут `hx-trigger` указывает событие, которое вызывает AJAX-запрос. `revealed` означает, что запрос
будет отправлен, когда элемент станет видимым.

Таким образом, когда пользователь прокручивает страницу вниз и она становится видимой, HTMX отправляет 
AJAX-запрос в Django, чтобы получить следующую страницу.

И так далее.

## Исходный код
[django-htmx-infinite-scroll](https://github.com/andgineer/django-htmx-infinite-scroll)