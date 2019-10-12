---
layout: post
lang: ru
ref: ncbi_pubmed_entrez_streaming
title: "Как извлечь информацию из части XML на примере NCBI (PubMed) Entrez API"
comments: true
tags: [pubmed, xml]
---
![](/images/eating-an-elephant-one-bite-at-a-time.png)

## Проблема NCBI Entrez

Мне было необходимо извлечь общую информацию о гене
из публичной БД NCBI.

К сожалению, их Entrez API на нужный мне запрос возвращает много ненужной мне
информации - мегабатйты.

Таким образом возникла задача получить только общее описание гена из
начала возвращаемого API XML, не загружая его полностью.

В Python для [xml.sax](https://docs.python.org/3.7/library/xml.sax.html) 
можно зарегистрировать обработчик, который будет получать уже извлеченные
из документа тэги на лету, еще в процессе разбора XML:

{% highlight python %}
parser = xml.sax.make_parser()
parser.setContentHandler(your_stream_handler)
{% endhighlight %}

Детальный пример использования такого обработчика можно увидеть в
[xml_stream.py](https://github.com/andgineer/http-stream-xml/blob/master/httpstreamxml/xml_stream.py)

Также есть возможность передавать в xml.sax документ XML кусочек за кусочком:

{% highlight python %}
parser = xml.sax.make_parser()
parser.feed(chunk)
{% endhighlight %}

Прекрасно, с парсингом частичного XML мы разобрались.

Что насчет частичной загрузки ответа с сервера? 
Самый простой случай если сервер поддерживает
[выдачу ответа частями](https://en.wikipedia.org/wiki/Chunked_transfer_encoding).

Но это не обязательное условие - мы можем просто прервать загрузку, как только
мы получим нужную нам часть.
Например [requests поддерживает поточную загрузку](https://requests.kennethreitz.org/en/master/user/advanced/#body-content-workflow):

{% highlight python %}
import requests

r = requests.get('https://httpbin.org/stream/20', stream=True)
for line in r.iter_lines():
    print(line)
{% endhighlight %}

Теперь вы готовы написать весь код.

Как пример вы можете посмотреть на 
[http-stream-xml](https://http-stream-xml.sorokin.engineer/en/latest/).
Задачу получения общего описания генов из NCBI Entrez можно решить с его 
помощью в две строки:

{% highlight python %}
from httpstreamxml import entrez

print(entrez.genes['myo5b'][entrez.GeneFields.description])
{% endhighlight %}