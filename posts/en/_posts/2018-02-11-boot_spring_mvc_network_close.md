---
layout: post
lang: en
ref: springnetworkclose
title: "Spring boot MVC emulate server error"
comments: true
tags: [java spring test]
---

For testing purporses I want to emulate server failure.

But if you use spring it will return some HTTP responce in any case, this is
robust framework.

But we can emulate server error if we close endpoint:

        @RequestMapping(...)
        @ResponseBody
        public byte[] processRequest(...
                                         final HttpServletRequest request,
                                         final HttpServletResponse response) {
            ...
            ((Response) response).getHttpChannel().getEndPoint().close();
            ...
        }

BTW I place that code not in the controller but in interceptor.

So I'd changed no server classes and this code for tests we can add or remove by changing
spring configuration.

[Article about that](/posts/en/2018-02-21-boot_spring_mvc_interceptor/)
