FROM alpine:latest

RUN apk add --no-cache bash curl gawk

LABEL "com.github.actions.name"="Create release"
LABEL "com.github.actions.description"="Create release"
LABEL "com.github.actions.icon"="command"
LABEL "com.github.actions.color"="blue"

ADD entrypoint.sh /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
