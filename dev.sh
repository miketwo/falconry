#!/bin/bash

docker build -t dev .
docker run -it -v $(pwd):/app --entrypoint "" dev /bin/bash
