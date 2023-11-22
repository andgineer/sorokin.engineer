---
layout: post
lang: en
ref: django_htmx_infinite_scroll
title: "Django Implementation of Infinite Scroll with HTMX"
comments: true
tags: [Python, HTMX, Django]
---

![](/images/python-scroll.png){:.post-title}

I will explain how to create an infinite, dynamically loaded list using Django and HTMX.
No JavaScript or CSS required.

I have also included Bootstrap for styling, but it's optional.

## TL;DR
```bash
git clone https://github.com/andgineer/django-htmx-infinite-scroll.git
cd django-htmx-infinite-scroll
. ./activate  # Note the dot at the beginning of the command
make init-db
make run
```

Now, open http://localhost:8000/ in your browser to view our infinite scroll list, which loads more pages as you scroll.

## How to Create Such an Application in Five Minutes
#### Create a Django Application
You should have Python and pip installed.
Install Django and create a project named core and an app named `django_htmx_infinite_scroll`:
{% highlight bash %}
pip install django faker
django-admin startproject core .
python manage.py startapp django_htmx_infinite_scroll
{% endhighlight %}

Add the app to INSTALLED_APPS in `core/settings.py`:
{% highlight python %}
INSTALLED_APPS = [
    ...
    'django_htmx_infinite_scroll',
]
{% endhighlight %}

#### Create a Model
Create a model in `django_htmx_infinite_scroll/models.py` similar to [BookPage](https://github.com/andgineer/django-htmx-infinite-scroll/blob/84d91ed61b86eb8c7c315ac4ab14b91f9a9101fe/django_htmx_infinite_scroll/models.py#L5).

Now, Django is aware of our model and can create a database table:
{% highlight bash %}
python manage.py makemigrations
python manage.py migrate
{% endhighlight %}

#### Populate the Database
To test, create records in the database. To do this, we need a Django command - add the contents of [add-pages](https://github.com/andgineer/django-htmx-infinite-scroll/blob/84d91ed61b86eb8c7c315ac4ab14b91f9a9101fe/django_htmx_infinite_scroll/management/commands/add-pages.py#L1)
 to the 
`django_htmx_infinite_scroll/management/commands/add-pages.py` file.

Now you can run `python manage.py add-pages`.

#### Create Views
Define two views in `django_htmx_infinite_scroll/views.py`, which can be copied from [views.py](https://github.com/andgineer/django-htmx-infinite-scroll/blob/84d91ed61b86eb8c7c315ac4ab14b91f9a9101fe/django_htmx_infinite_scroll/views.py#L1).

#### Add URLs
To access these views, we need to add URLs.

Add a link to the app's URL in core/urls.py:
{% highlight python %}
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("django_htmx_infinite_scroll.urls")),
]
{% endhighlight %}

Create django_htmx_infinite_scroll/urls.py:
{% highlight python %}
from django.urls import path
from . import views

urlpatterns = [
    path("", views.book, name="book"),
    path("book-page", views.book_page, name="book-page"),
]
{% endhighlight %}

The first URL will invoke the book view, which displays book pages.
The second URL will serve book pages, both for the initial display of the first pages and for loading the next book page via HTMX as you scroll.

#### Create Templates
We are almost done.
Now, create templates for our views.

We will create a template hierarchy to avoid duplicating code.

Copy the files from [templates/](https://github.com/andgineer/django-htmx-infinite-scroll/tree/main/django_htmx_infinite_scroll/templates) 
to the `django_htmx_infinite_scroll/templates` directory.

#### Start the Server
Now you can start the server and see the result:
{% highlight bash %}
python manage.py runserver
{% endhighlight %}

Open http://localhost:8000/ in your browser, and you will see a scrollable list of pages.

## Code Explanation
## Source Code
[django-htmx-infinite-scroll](https://github.com/andgineer/django-htmx-infinite-scroll)