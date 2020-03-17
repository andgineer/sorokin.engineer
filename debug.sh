# Build and run docker container with jekyll for
# live debugging
# if you use Visual Studio Code you do not need that file - VS Code run
# Jekyll in docker automatically - see .devcontainer/
docker build . -t sorokin.engineer
docker run --rm -it \
    --name sorokin.engineer \
    -p 4000:4000 \
    --mount type=bind,source="$(pwd)"/,target=/workspaces/sorokin.engineer \
    sorokin.engineer
