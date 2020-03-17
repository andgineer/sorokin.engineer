---
layout: post
lang: ru
ref: bootprint_openapi_russian
title: "OpenAPI(swagger): Генерация рускоязычного описание API"
comments: true
tags: [api, web, swagger, bootprint]
redirect_from: "/posts/ru/bootprint_openapi_russian/"
---

![](/images/bootprint.png){:.post-title}

Заказчик у нас - московское метро, из этого возникают странные задачи типа необходимости
иметь фиксированное, а не живое описание API, причем на русском языке.

Уже первая задача непростая, ведь гораздо удобнее для изучения [Open API](http://swagger.io/)
использовать [swagger ui](http://swagger.io/swagger-ui/), который, например, входит
в генерируемые с помощью swagger codegen сервера.

Но заказчику надо что-то, что он может положить в шкаф.
То, что выходит из swagger codegen таковым не является.

Ок, нашелся [bootprint-openapi](https://github.com/bootprint/bootprint-openapi).

Вторая проблема, с русификацией, решалась несложно - я [форкнул](https://github.com/andgineer/bootprint-openapi)
проект и буквально за полчаса получил устраивающую нас русификацию (она не совсем точна с
точки зрения OpenAPI, но она отражает именно то, что мы хотели показать заказчику).

Правда, как обычно, двумя проблемами никогда не заканчивается, потом возникла третья,
но это уже [другая история](athena_web_page_to_pdf.html).
