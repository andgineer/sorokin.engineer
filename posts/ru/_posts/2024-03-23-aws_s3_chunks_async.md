---
layout: post
lang: ru
ref: s3_chunks_async
title: "aioS3: Асинхронная загрузка файлов из AWS S3 по частям"
comments: true
tags: [aws s3 async python]
---

![](/images/s3aio.png){:.post-title}

[aiobotocore](https://aiobotocore.readthedocs.io/en/latest/) может читать большие файлы по частям.

Чтобы прочитать файл полностью, вам нужно создать цикл вроде этого:

```python
resp = yield from s3.get_object(Bucket='mybucket', Key='k')
stream = resp['Body']
try:
    while True:
      chunk = yield from stream.read(1024)
      ...
      if len(chunk) > 0:
          break
finally:
  stream.close()
```

Но если вам нужен объект, похожий на файл, для чего-то вроде `pickle.load()` или `json.load()`, вы не можете читать по
частям - он будет читать весь файл. 

В некоторых случаях это может быть неэффективно - например, `pickle` читает объекты по кускам, вам не нужно
загружать весь файл в память для этого.

С [aioS3](https://github.com/andgineer/aios3/actions) `stream()` у вас есть 
[интерфейс](https://andgineer.github.io/aios3/reference/#aios3.file.stream), похожий на файл, с настраиваемым
размером куска.
