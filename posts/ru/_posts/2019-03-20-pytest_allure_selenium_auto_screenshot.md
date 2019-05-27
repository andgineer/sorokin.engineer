---
layout: post
lang: ru
ref: pytest_allure_selenium_auto_screenshot
title: "Как автоматически делать скриншот при падении Selenium теста в py.test"
comments: true
tags: [Python, test, pytest, selenium, webdriver, allure]
redirect_from: "/posts/en/pytest_allure_selenium_auto_screenshot/"
---
![](/images/allure-report.png){:.post-title}

Показанный ниже код будет автоматически делать скриншоты при неуспехе теста.
Он делает это только для Selenium тестов различая их по имени фикстуры
с Selenium webdriver `browser` - если вы используете другое имя то вам надо 
поправить этот код.

Я использую allure для построения отчетов по тестам и данный код помещает
скриншот в отчет allure.

<script src="https://gist.github.com/masterandrey/4ec6d58857bb8689907c87f63475525f.js"></script>

В итоге вы получите отчет похожий на приведеный на картинке выше.

Вы можете посмотреть на 
[полный код](https://github.com/masterandrey/e2e-tests) тестов.

Или узнать как с минимальными усилиями можно развернуть Selenium + Allure 
конфигурацию для тестов
[из моей статьи](https://sorokin.engineer/posts/ru/e2e_tests.html).
