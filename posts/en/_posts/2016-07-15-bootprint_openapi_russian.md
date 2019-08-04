---
layout: post
lang: en
ref: bootprint_openapi_russian
title: "OpenAPI(swagger): Exportable documentation"
comments: true
tags: [api, web, swagger, bootprint]
redirect_from: "/posts/en/bootprint_openapi_russian/"
---

![](/images/bootprint.png){:.post-title}

For the project we use [Open API](http://swagger.io/).

Our customer ask for API documentation - [swagger live UI](http://swagger.io/swagger-ui/) 
was not good enough for him.

He want something that he can place on shelf.

Ok here it is [bootprint-openapi](https://github.com/bootprint/bootprint-openapi).

And of cause we wanted Russian version so I [forked](https://github.com/masterandrey/bootprint-openapi)
bootprint-openapi and it took about half and hour to localize it. The project is based on handle bars
and all strings to localize neatly in one place.
It's a pity I cannot merge my localization with the project because bootprint-openapi does not support 
such a thing and it's not easy to figure out how to do that.

After that we had another problem with our resourceful customer 
[but this is another story](athena_web_page_to_pdf.html).
