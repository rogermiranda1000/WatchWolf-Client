# WatchWolf - MC Client
A Python library to test Minecraft Plugins in the client side.

## Dependencies
- [Docker](https://www.docker.com/get-started/)
- Python image: `docker pull python:3.10-slim-bullseye`
- Build the image: `docker build --tag clients-manager .`

## Launch
- Run the docker container: `sudo docker run -i --rm --name ClientsManager -p 7000:7000 clients-manager:latest`