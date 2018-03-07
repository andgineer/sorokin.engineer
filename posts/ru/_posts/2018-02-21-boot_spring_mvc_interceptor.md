---
layout: post
lang: ru
ref: springinterceptor
title: "Spring boot MVC interceptor"
comments: true
tags: [java, spring, test]
---

Мне было необходимо добавить в spring сервер имитацию ошибок.
Причем сделать это так, чтобы не менять исходный код сервера и иметь возможность
собрать сервер без этой, нужной только для тестирования, функциональности.

Для этого я использовал перехватчики запросов spring (interceptor).
В моем случае предобработчик вызывается до кода сервера, если необходимо имитирует
нужную тесту ситуацию, а дарлее уже будет вызван штатный обработчик сервера.

Тест сообщает о необходимости имитации определенных ситуацих с помощью дополнительных
 `http headers`, которые по стандарту `HTTP` сервер должен игнорировать, поэтому
 управление прозрачно для основного кода сервера.

Код перехватчика:

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

Мы можем сформировать свой ответ в `response` (тогда надо вернуть `false` и штатный обработчик уже не будет вызываться), или сказать spring, что надо вызвать штатный обработчик (вернуть
`true`).

Конфигурационный код, который подключает перехватчик к spring приложению:

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
