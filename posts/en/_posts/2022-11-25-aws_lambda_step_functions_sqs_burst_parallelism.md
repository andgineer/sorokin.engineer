---
layout: post
lang: en
ref: aws_lambda_step_functions_sqs_burst_parallelism
title: "Unleash an explosive fleet of Lambda functions"
comments: true
tags: [aws, serverless, lambda, sqs, step functions]
---

![](/images/step_functions_map.png){:.post-title}

## Unexpected Parallelism Gotcha

For some massive scientific calculations, where thousands of small functions are required, we encountered an unexpected challenge. 
Our initial instinct led us to consider AWS Lambda as the ideal solution. 
After all, it seemed perfectly suited for the job, right?

With each function taking only 5-6 seconds, we had no reason to anticipate any problems. 
Excited by the potential efficiency, I embarked on creating a simple PoC using SQS and Lambda.

To our surprise, the job took a whopping 20 minutes to complete, despite having less than 1000 functions to calculate. 
Perplexed and determined to find a more efficient approach, I decided to rewrite the code using Step Functions and the map state.

Yet, to my dismay, even with this new implementation, it still took 20 minutes to execute. 
Frustrated, I sought solace in the depths of the AWS documentation and stumbled upon a crucial piece of information.

As I delved into the fine print, I discovered that Step Functions map state, much like SQS Lambda, has a limitation. 
It allows the spawning of only 40 lambda function instances per minute. This meant that if you have 1000 functions to calculate, 
it takes 1000/40 = 25 minutes.

## The Solution
With understanding of the problem, the solution is simple. 

Some guys in this case use recursive map states within Step Functions.

But in our case we just created a master lambda function that spawn 1000 workers lambda functions.

The impact was nothing short of extraordinary. Our calculations now blazed through at an unprecedented speed.

As a final note, if you find yourself needing to exceed the 1000-parallel-function threshold, fear not! 
You can simply reach out to AWS support and request an increase in your quota, and the best part? It won't cost you a dime.
