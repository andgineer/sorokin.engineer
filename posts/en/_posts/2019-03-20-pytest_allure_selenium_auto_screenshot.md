---
layout: post
lang: en
ref: pytest_allure_selenium_auto_screenshot
title: "Py.test automatic Selenium screenshot"
comments: true
tags: [Python, test, pytest, selenium, webdriver, allure]
redirect_from: "/posts/en/pytest_allure_selenium_auto_screenshot/"
---
![](/images/allure-report.png){:.post-title}

You can write simple pytest hook to take Selenium webdriver screenshots
automatically each time test fail.
It recognize Selenium tests by fixture name `browser` so if you use
another name for Selenuim webdrive you should change it.
Full tests code you can find on [github](https://github.com/masterandrey/e2e-tests)

If you use allure you can nicely attach the screenshots to test report
as show in code below.

<script src="https://gist.github.com/masterandrey/4ec6d58857bb8689907c87f63475525f.js"></script>

The result would be like on picture above.

In my [article](https://masterandrey.com/posts/en/e2e_tests.html)
I explain how you can set up powerful test infrastructure in no time.
