---
layout: post
lang: ru
ref: 2021-07-16_jenkins_load_env_vars_with_expanding
title: "Jenkins загрузка переменных из файла с подстановками"
comments: true
tags: [jenkins, groovy, python, bash]
---

![](/images/jenkins.png){:.post-title}


Предположим вам необходимо использовать `.env` файлы в Jenkins.

`rabbitmq.env`

    RABBITMQ_DEFAULT_USER=guest

`celery.env`

    AMQP_USERNAME=${RABBITMQ_DEFAULT_USER}

Дженкинс умеет загружать groovy-файлы но предположим вы используете эти .env файлы где-то еще
и не можете конвертировать их в groovy скрипты.

Значит вам необходима функция, которая загрузит `.env` файл в переменные Jenkins environment
(`env.*`).

Далее приведена Jenkins(groovy) функция, которая загружает`.env` файл (на каждой строке `key=value`) 
в Jenkins `env`-переменные.
После ее работы вы сможете использовать `env.AMQP_USERNAME` в вашем Jenkinsfile.

<script src="https://gist.github.com/andgineer/155a8ef1a4e4e29bd68ee9ef1d47b9ed.js"></script>

Однако эта функция не подставляет значение переменных. То есть `env.AMQP_USERNAME`
будет буквально строкой `${RABBITMQ_DEFAULT_USER}`.

Если вам необходимо подставить все `${..}` то в этом вам поможет следующая комбинация
groovy и Питона:

<script src="https://gist.github.com/andgineer/aee9022fad89cb8b87e931c8b7de7321.js"></script>
<script src="https://gist.github.com/andgineer/17f90aaa02a7042232e32aed9c4bacca.js"></script>

Как их использовать в декларативном пайплайн Jenkinsfile:

{% highlight groovy %}
pipeline {
    // ...
    stages {
        // ...
        stage('Prepare environment') {
            steps {
                script {
                // ...
                vars_text = sh(
                    script: """python expand_vars.py \
                            rabbitmq.env \
                            celery.env
                            """,
                    returnStdout: true
                )
                loadVarsFromText(vars_text)
                // ...
                }
            }
        }
        // ...
    }
    // ...
}
// ...
private void loadVarsFromText(String text) {
    // ...
}
{% endhighlight %}

Эта техника поможет вам загрузить в переменные Jenkins `.env` файл
с подстановкой значений переменных, так что `env.AMQP_USERNAME` == `guest`
