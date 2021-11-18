My personal blog [sorokin.engineer](http://sorokin.engineer)

You do not need local Jekyll installation if you just change file and put it on github.

But it always usefull to check it locally before publishing.

In that case you have to install Jekyll and plugins for github pages (the plugins are listed in `Gemfile`).

## Linux (Ubuntu)

[Install rbenv](https://github.com/rbenv/rbenv#installing-ruby-versions)

Add `/home/<your user name>/.rbenv/bin:` into `PATH` (`~/.bashrc`). and add `eval "$(rbenv init -)"` after this line in `~/.bashrc`.

    sudo apt-get install ruby-dev build-essential libssl-dev libreadline-dev zlib1g-dev
    rbenv install 2.5.7
    rbenv global 2.5.7
    sudo gem install bundler

    # cd to sorokin.engineer folder
    bundle


## Windows

Use the Dockerfile in [Docker](https://docs.docker.com/docker-for-windows/install/)
or [Visual Studio Code](https://code.visualstudio.com/docs/setup/windows) 
integration (.devcontainer/).

Run the docker container or run in VS Code terminal the command below:

    jekyll serve

## MacOS

https://jekyllrb.com/docs/installation/macos/

And after that:
 
   bundler

### Reinstall after MacOS update

    brew install ruby
    echo 'export GEM_HOME=$HOME/gems' >> ~/.bashrc
    echo 'export PATH=$HOME/gems/bin:$PATH' >> ~/.bashrc
    echo 'export PATH="/usr/local/opt/ruby/bin:$PATH"' >> ~/.bashrc
    . ~/.bashrc
    gem install jekyll bundler
    
### Run

    jekyll serve

