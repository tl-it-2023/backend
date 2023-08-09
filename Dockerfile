FROM ubuntu:latest
LABEL authors="nn"

ENTRYPOINT ["top", "-b"]