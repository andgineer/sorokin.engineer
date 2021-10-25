---
layout: post
lang: en
ref: 2021-08-25-github-actions-release-pypi-python-package
title: "Auto publish pip package on git tag and creating github release"
comments: true
tags: [python, guthub actions, git]
---

![](/images/pip.jpg){:.post-title}

# Github action to upload PIP package and create Github release

If you created PIP package, for sure you want to know exactly what source code version was published as all
the versions you created on pypi.org.

This is not enough to write down git commit. Because you need strong link between code and the moment when you 
published the version.

One approach - to use git tag and publish the commit with the tag.
This way you can be sure what commit was published.

With Github actions you can automate that so each time you create new version tag, 
Github actions would upload the version.

# Result you will have

On `./verup.sh bug` it will
- create version tag with increased last number
- update `version.py` in your package
- publish the version in PIP (on pypi.org)
- create Github release with convenient link to the pypi version page

# Adaptation for your project

Use [aioS3 repo](https://github.com/andgineer/aios3) as template.

## activate.sh

To work with the project run 

    . ./activate.sh

Please note the first `.` this is how we source the script so it can activate virtual environment.
This script will create ethe environment if it does not exists.

It is always safe just `rm -r venv` if for some reason you want fresh installation, for
example to upgrage dependencies. 
On the next run `activate.sh` will recreate it.

[activate.sh](https://github.com/andgineer/aios3/blob/master/activate.sh) also install your package in dev mode `pip install -e .` so you can import from it.

If you use the same [requirements.txt](https://github.com/andgineer/aios3/blob/master/requirements.txt) 
as I do you can leave this file intact.

Just do not forget to install [virtualenv](https://virtualenv.pypa.io/en/stable/installation.html).

# setup.py

Change `aios3` in line [from src.aios3 import version](https://github.com/andgineer/aios3/blob/19b3a6b4b6904883fa8a3a25e474983a1563b02e/setup.py#L9) with your package name. 

PIP will auto-discover all packages inside `src` folder.

# verup.sh

Use `verup.sh` to create version tags, do not create the tags manually.

The version consists of three digits:

    release.feature.bug

For example to increase last number in version use command

    ./verup.sh bug

To increase 1st

    ./verup.sh release

This script also updates `version.py` in sources.
You can use this file to show version from you application.

And this file is used in `setup.py` to set your package version while uploading to `pypi.org`.

Do not forget to edit [VERSION_FILES](https://github.com/andgineer/aios3/blob/19b3a6b4b6904883fa8a3a25e474983a1563b02e/verup.sh#L5) 
in `verup.sh` (there could be many file locations separated by space).

# Github action .github/workflows/pip_publish.yml

In line [body: https://pypi.org/project/aios3/${{ env.RELEASE_VERSION }}/](https://github.com/andgineer/aios3/blob/19b3a6b4b6904883fa8a3a25e474983a1563b02e/.github/workflows/pip_publish.yml#L47) change `aios3` with your package name.

