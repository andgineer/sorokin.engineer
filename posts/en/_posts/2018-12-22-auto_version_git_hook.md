---
layout: post
lang: en
ref: auto_version_git_hook
title: "Automatic tag sources with version (not only Python) - GIT hook"
comments: true
tags: [Python Git bash]
redirect_from: "/posts/en/auto_version_git_hook.md/"
---

![](/images/git-secret-big.png){:.post-title}

## Problem

You want to know version of the application.

For mature development flow (development - testing - demo - production)
there is alway version. 
But for the price - somebody set it (for example as `git tag`).

But we need versions for our internal process like deployment to
develpment server.

For this purposes we can use `git hooks`.
This is scripts that run locally by git for different events. 
For example before commit.

Script below saves date and time to some file and add
this file to the commit.

Name this file as `git_hook_add_commit_date.sh`.

{% highlight bash %}
{% include src/git_precommit.sh %}
{% endhighlight %}

File with date and time will be inside your source code.

So you can use it like this: 

{% highlight python %}
{% include src/version.py %}
{% endhighlight %} 

In security reasons `git hooks` you have to install
by yourself on each machine you use for development.

Script below installs our script as `pre-comit git hook`.

{% highlight bash %}
{% include src/git_hook_install.sh %}
{% endhighlight %}

I wanted to add commit message.
But I have not found way for this.
The message you can get in the `git hook commit-msg`.
But if you add something to commit on this phase (for example as
`git commit --amend`) git will fail the commit with message
that `HEAD` was changed.

If you know how to do that please let me know.
