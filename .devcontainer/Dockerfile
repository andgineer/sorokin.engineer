FROM ruby:2.5

# throw errors if Gemfile has been modified since Gemfile.lock
RUN bundle config --global frozen 1

# we need bundler v2
RUN gem update --system \
    && gem install bundler -v 2.1.4

# we need it at container build time so we cannot use mount that VS Code will create later
COPY Gemfile Gemfile.lock ./

RUN bundle install

EXPOSE 4000

WORKDIR /workspaces/sorokin.engineer

CMD ["jekyll serve"]
