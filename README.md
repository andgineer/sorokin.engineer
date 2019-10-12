My personal blog [andrey.engineer](http://andrey.engineer)

## Install Jekyll for local debug (MacOS)

https://jekyllrb.com/docs/installation/macos/

## Reinstall after MacOS update

    brew install ruby
    echo 'export GEM_HOME=$HOME/gems' >> ~/.bashrc
    echo 'export PATH=$HOME/gems/bin:$PATH' >> ~/.bashrc
    echo 'export PATH="/usr/local/opt/ruby/bin:$PATH"' >> ~/.bashrc
    . ~/.bashrc
    gem install jekyll bundler
    
## Run locally

    jekyll serve

