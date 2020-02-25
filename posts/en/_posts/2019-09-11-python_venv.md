---
layout: post
lang: en
ref: python_venv
title: "How to house keep your Python environment"
comments: true
tags: [python, virtualenv]
---
![](/images/workenv.png){:.post-title}

I am sure you want your work place to be tidy and efficiently organized.
And this is about your Python environment as well. 

If you want it to be predictable and you do not like to spend hours on Stackoverflow in search how 
to fix your environment gone out of control you just have to use virtual environment for each and 
every python project that you are involved in.

Luckily starting from [Python 3.6](https://docs.python.org/3.6/library/venv.html) this is super easy! 
You do not even have to install [virtualenv](https://virtualenv.pypa.io/en/latest/). 
All batteries now are included!

    python3 -m venv <venv folder name>
    
For Windows use

    python -m venv <venv folder name>
    
This command will create in `<venv folder name>` Python virtual environment that incapsulates all 
Python libraries.

To "activate" it (please note first `.` this is shortcut for [source](https://superuser.com/questions/176783/what-is-the-difference-between-executing-a-bash-script-vs-sourcing-it))
    
    . <venv folder name>/bin/activate 
    
For Windows use

    <venv folder name>\Scripts\activate.bat

After activation all libraries will be used from the environment. And when you install something with
`pip install` it will change only this local environment and wont break your system or change any other
environments.        
    
To exit from the environment

    deactivate    
    
To make it even simpler I want to share with you the very simple script `activate.sh`:

<script src="https://gist.github.com/andgineer/345eac0abb9149c165b64bf0d9c8694e.js"></script>

In linux you run (note first `.`)

    . ./acivate.sh
    
It will will create virtual environment if it is not exist. Also it installs in the environment 
Python packages listed in the file `requirements.txt`. If the environment already exists the script
does nothing (see the check on line 25).
  
After that the script activates the environment (line 32).
In the variable `PYTHON` (line 7) inside the script you specify Python version you need. And you can change the 
virtual environment folder name in variable `VENV_FOLDER` (line 6).

Line 14..22 checks that you do [source](https://superuser.com/questions/176783/what-is-the-difference-between-executing-a-bash-script-vs-sourcing-it) the script (call it with command `source` or `.`).

If you get error `.. 'ensurepip', '--upgrade', '--default-pip']' returned non-zero exit status 1` 
that means you have not installed module `ensurepip` for the Python version you specified in the
script (variable `PYTHON`) and you need to install it. For example for python3.7 in Ubuntu:

    sudo apt-get install python3.7-venv
