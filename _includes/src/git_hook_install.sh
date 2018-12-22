#!/usr/bin/env bash
if [ ! -f .git/hooks/pre-commit ] ; then
    ln -s $PWD/git_hook_add_commit_date.sh .git/hooks/pre-commit
fi
