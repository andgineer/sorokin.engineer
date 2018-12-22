---
layout: post
lang: ru
ref: springnetworkclose
title: "Spring boot MVC имитация проблем с сервером"
comments: true
tags: [java, spring, test]
redirect_from: "/posts/ru/boot_spring_mvc_network_close/"
---
![](/images/failure.jpg){:.post-title}

С целью тестирования мне потребовалось имитировать проблему сервера, не возвращающего
ответ.

Но при использовании фреймворка spring это не так просто - он разработан с точки зрения
надежности и мы всегда вернем какой-то HTTP-ответ, что бы ни произошло в приложении.

Однако мы можем получить желаемое поведение, если закроем сам endpoint в обработчике
запросов контроллера:

        @RequestMapping(...)
        @ResponseBody
        public byte[] processRequest(...
                                         final HttpServletRequest request,
                                         final HttpServletResponse response) {
            ...
            ((Response) response).getHttpChannel().getEndPoint().close();
            ...
        }

Кстати, сам этот тестирующий код был встроен в сервер как интерсептор, что позволило во-1х
никак не изменять классы сервера, а во-2х иметь простой способ, меняя spring-конфигурацию
сервера, добавлять или убирать необходимый для тестов код.

[В этой статье описано, как это сделано](/posts/ru/boot_spring_mvc_interceptor/)