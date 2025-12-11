FROM ubuntu:latest
LABEL authors="jschrott"

ENTRYPOINT ["top", "-b"]