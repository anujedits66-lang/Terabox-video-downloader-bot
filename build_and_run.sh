#!/bin/bash

# Build the Docker image with the tag 'my-telegram-bot'
docker build -t my-telegram-bot .

# Run the Docker container in detached mode and map port 80 on the host to port 80 in the container
docker run -d -p 80:80 my-telegram-bot
