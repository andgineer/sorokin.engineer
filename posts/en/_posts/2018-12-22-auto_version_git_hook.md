---
layout: post
lang: en
ref: auto_version_git_hook
title: "Automatically add version to sources (not only Python) - GIT hooks"
comments: true
tags: [Python Git bash]
redirect_from: "/posts/en/auto_version_git_hook.md/"
---

![](/images/git-secret-big.png){:.post-title}

## Problem

You want to know version of the application instance.

For mature development flow (development - testing - demo - production)
there is always version. 
But for the price - somebody has to set it (for example as `git tag`).

But we need versions for our internal process like deployment to
development server.

For this purposes we can use `git hooks`.
This is scripts that run locally by `git` for different events. 
For example before commit.

Script below saves date and time to some file and add
this file to the commit.

Name this file as `git_hook_add_commit_date.sh`.

{% highlight bash %}
{% include src/git_precommit.sh %}
{% endhighlight %}

As it's inside your source code you can use it like this: 

{% highlight python %}
{% include src/version.py %}
{% endhighlight %} 

For security reasons you have to install `git hooks`
by yourself on each machine you use for development.

Script below installs our script as `pre-comit git hook`.

{% highlight bash %}
{% include src/git_hook_install.sh %}
{% endhighlight %}

In fact I wanted to add commit message as well.
But I have not found way for doing this.
Commit message you can easily get in the `git hook commit-msg`.
But if you add something to commit on this phase (for example as
`git commit --amend`) git will fail the commit with message
that `HEAD` was changed.

If you know how to do that please let me know.
