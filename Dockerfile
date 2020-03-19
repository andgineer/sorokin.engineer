FROM ruby:2.5

# throw errors if Gemfile has been modified since Gemfile.lock
RUN bundle config --global frozen 1

# we need bundler v2
RUN gem update --system \
    && gem install bundler -v 2.1.4

# we need the files with Ruby dependancies at container build time so we cannot use files from repository
https://raw.githubusercontent.com/andgineer/sorokin.engineer/master/Gemfile
https://raw.githubusercontent.com/andgineer/sorokin.engineer/master/Gemfile.lock

RUN bundle install

EXPOSE 4000

WORKDIR /workspaces/sorokin.engineer

CMD ["jekyll serve"]
