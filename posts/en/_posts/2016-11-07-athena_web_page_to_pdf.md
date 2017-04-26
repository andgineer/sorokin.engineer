---
layout: post
lang: en
ref: athena_web_page_to_pdf
title: "Beautiful PDF with Athena"
comments: true
summary: ...Beautiful PDF with Athena...
tags: [PDF, web, docker, athena]
---

![](/images/athena.png){:.post-title}

Our customer wanted APIs documentation as PDF file.
We document our APIs in [Open API](http://swagger.io/).
Attempts to export with help of [pandoc](http://pandoc.org/)
or MS Office / Libre Office export was a fail - broken pages.
May be that was because of bug in the [bootprint-openapi](https://github.com/bootprint/bootprint-openapi)
that I found and fixed later - I do not know.

I did not want to create mine version of [bootprint-openapi](https://github.com/bootprint/bootprint-openapi),
that produce html good enough for MS Word - too much effort for the task.

And I found just a beautiful project
[Athena Elegant PDF conversion](http://www.athenapdf.com/).

It has two features to be beautiful.

In 1st PDF is just exact representation of what I see in web browser.
In fact it take screen shot so no wonder but still great.

I 2nd Athena developers made their product sxtremly easy to use.

You want web service to convert on the fly? Ok:
{% highlight bash %}
docker pull arachnysdocker/athenapdf-service
http://<docker-address>:8080/convert?auth=arachnys-weaver&url=http://blog.arachnys.com/
{% endhighlight %}

I wanted convert files beforehand (that is very fast process, 1-2 seconds, but still not pleasant pause).

Ok for that I use Makefile:
{% highlight bash %}
for API in docker/docs/target/*/; \
    do docker run --rm -v ${PWD}:/converted/ arachnysdocker/athenapdf athenapdf $${API}/index.html $${API}/$$(basename $${API}).pdf; \
done
{% endhighlight %}

In logs I see a lot of errors like:
{% highlight bash %}
Xlib:  extension "RANDR" missing on display ":99".
{% endhighlight %}

but everithing works fine so I did not bother to understand why I have this errors in logs.

And you have to take into account this Electron's bug (athena is written with Electron):
[Duplication of thead, and other table related issues](https://github.com/arachnys/athenapdf/issues/68)

My workaround:
{% highlight bash %}
sed -i "\$athead {display:table-row-group;}" /docs/$API/main.css
{% endhighlight %}

I am still in wonder from Docker - one line and your not so small problem is solved!
