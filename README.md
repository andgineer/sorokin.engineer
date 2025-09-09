My personal blog [sorokin.engineer](http://sorokin.engineer)

You do not need local Jekyll installation if you just change files and push to GitHub.

But it's always useful to check it locally before publishing.

In that case you have to install Jekyll and plugins for GitHub Pages (the plugins are listed in `Gemfile`).

## Linux (Ubuntu)

[Install rbenv](https://github.com/rbenv/rbenv#installing-ruby-versions)

Add `/home/<your user name>/.rbenv/bin:` to `PATH` (`~/.bashrc`) and add `eval "$(rbenv init -)"` after this line in `~/.bashrc`.

    sudo apt-get install ruby-dev build-essential libssl-dev libreadline-dev zlib1g-dev
    rbenv install 2.5.7
    rbenv global 2.5.7
    sudo gem install bundler

    # cd to sorokin.engineer folder
    bundle


## Windows

Use the Dockerfile with [Docker](https://docs.docker.com/docker-for-windows/install/)
or [Visual Studio Code](https://code.visualstudio.com/docs/setup/windows) 
integration (`.devcontainer/`).

Run the Docker container or run in VS Code terminal the command below:

    jekyll serve

## MacOS

[Install Jekyll](https://jekyllrb.com/docs/installation/macos/)

And after that:
 
    bundle

### Reinstall after MacOS update

        brew install rbenv
        rbenv install 3.2.2
        rbenv global 3.2.2
        echo 'eval "$(rbenv init - zsh)' >> ~/.zshrc
        gem install --user-install bundler jekyll

        bundle install

Add `/Users/<username>/.gem/ruby/3.2.0/bin` to PATH (in `.zshrc`).
    
### Run

    jekyll serve

## Analytics

- [Google Analytics](https://analytics.google.com) (Property: G-HF63EZ3FXE)
- [Yandex Metrika](https://metrika.yandex.com) (Counter: 53999143)
