#!/usr/bin/env bash
if [ ! -f .git/hooks/pre-commit ] ; then
    ln -s $PWD/git_hook_pre_commit.sh .git/hooks/pre-commit
    ln -s $PWD/git_hook_post_commit.sh .git/hooks/post-commit
fi
