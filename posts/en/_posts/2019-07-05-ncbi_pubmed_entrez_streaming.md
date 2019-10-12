---
layout: post
lang: en
ref: ncbi_pubmed_entrez_streaming
title: "How to parse only small part of XML from NCBI (PubMed) Entrez API"
comments: true
tags: [pubmed, xml]
---
![](/images/eating-an-elephant-one-bite-at-a-time.png)

## NCBI Entrez problem

For my project I need general gene information from NCBI database.

The problem is Entrez API returns really huge responses, with many megabytes.

The gene summary I need is at the very beginning. So I want only beginning of the
response.

How to get just first part of XML and extract information from this invalid
partial XML?

In Python [xml.sax](https://docs.python.org/3.7/library/xml.sax.html) we can register
content handler that will handle all XML tags on the fly. During the XML
parsing:

{% highlight python %}
parser = xml.sax.make_parser()
parser.setContentHandler(your_stream_handler)
{% endhighlight %}

Example how to use such an handler see in
[xml_stream.py](https://github.com/andgineer/http-stream-xml/blob/master/httpstreamxml/xml_stream.py)

And we can feed XML chunk by chunk to the xml.sax:

{% highlight python %}
parser = xml.sax.make_parser()
parser.feed(chunk)
{% endhighlight %}

Ok this is parsing part.

What about loading? Well, generally HTTP server could support 
[chunked transfer](https://en.wikipedia.org/wiki/Chunked_transfer_encoding).

But even if it does not we can just disconnect at the moment we got all the
data we need.
For example [requests supports streaming](https://requests.kennethreitz.org/en/master/user/advanced/#body-content-workflow):

{% highlight python %}
import requests

r = requests.get('https://httpbin.org/stream/20', stream=True)
for line in r.iter_lines():
    print(line)
{% endhighlight %}

Now you can write all the code by yourself.
Or use [http-stream-xml](https://http-stream-xml.sorokin.engineer/en/latest/):

{% highlight python %}
from httpstreamxml import entrez

print(entrez.genes['myo5b'][entrez.GeneFields.description])
{% endhighlight %}