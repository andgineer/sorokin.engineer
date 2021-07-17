---
layout: post
lang: en
ref: 2021-07-16_jenkins_load_env_vars_with_expanding
title: "Jenkins load env vars from file with expanding"
comments: true
tags: [jenkins groovy python bash]
---

![](/images/jenkins.png){:.post-title}

Suppose you have some `.env` files that you would like to use in Jenkins.

`rabbitmq.env`

    RABBITMQ_DEFAULT_USER=guest

`celery.env`

    AMQP_USERNAME=${RABBITMQ_DEFAULT_USER}

If you use this files somewhere else, for example in Docker, you do not want to convert 
them to groovy files that natively loaded by Jenkins.

So you need some code that will load this `.env` file into Jenkins environment 
vars (`env.*`).

This simple groovy function will load `.env` file (with `key=value` on each line) into 
Jenkins `env`.
So after that you could use `env.AMQP_USERNAME` in you Jenkinsfile.

<script src="https://gist.github.com/andgineer/155a8ef1a4e4e29bd68ee9ef1d47b9ed.js"></script>

The problem with this function - it won't expand vars. That means that `env.AMQP_USERNAME`
will be equal string `${RABBITMQ_DEFAULT_USER}`.

If you want all environment vars like `${..}` to be expanded (substituted with their 
respective values) we should find another solution.

For this purpose I created this simple groovy function and some Python code:

<script src="https://gist.github.com/andgineer/aee9022fad89cb8b87e931c8b7de7321.js"></script>
<script src="https://gist.github.com/andgineer/17f90aaa02a7042232e32aed9c4bacca.js"></script>

How to use it in declarative Jenkinsfile:

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

With this approach Jenkins env vars will be loaded from `.env` file and expended 
so `env.AMQP_USERNAME` == `guest`
