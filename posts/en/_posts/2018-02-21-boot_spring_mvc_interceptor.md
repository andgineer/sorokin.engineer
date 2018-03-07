---
layout: post
lang: en
ref: springinterceptor
title: "Spring boot MVC interceptor"
comments: true
tags: [java, spring, test]
---

For test purposes I wanted to add error emulation to our spring server.
But I did not want to modify its sources and wanted ability to compile server without
this test functionality.

For that I used spring interceptor.
In my case interceptor works before server controller.

Test communicates with the interceptor thru additional `http headers`.
As specified in `HTTP RFC` server shoul ignore unknown headers so this is transparent
for it.

Interceptor source:

    @Controller
    public class EmulatorInterceptor implements HandlerInterceptor {

        @Override
        public boolean preHandle(HttpServletRequest request,
                                 HttpServletResponse response, Object object) {
            // check http-header for test command
            final String emulateError = request.getHeader(EMULATE_HEADER);
            if (Objects.equals(EMULATE_NETWORK_CLOSE, emulateError)) {
                ((Response) response).getHttpChannel().getEndPoint().close();
                return false;  // finish request processing
            }
            return true;  // continue request processing in the server controller
        }
    }

We can make our answer in `response` (and return `false` so spring won't call server controller), or we can return `true` and spring will call server controller.

Configuration class to add the interceptor to the spring application:

    @Component
    public class InterceptorConfig implements WebMvcConfigurer {

        private final EmulatorInterceptor emulatorInterceptor;

        @Autowired
        public InterceptorConfig(EmulatorInterceptor emulatorInterceptor) {
            this.emulatorInterceptor = emulatorInterceptor;
        }

        @Override
        public void addInterceptors(InterceptorRegistry registry) {
            registry.addInterceptor(emulatorInterceptor);
        }
    }
