#!/usr/bin/env bash
FILE=build_timestamp
git add "$FILE"
git commit --amend -C HEAD --no-verify
