FROM --platform=$BUILDPLATFORM python:3.9-slim
MAINTAINER django@datama.fr

LABEL "com.github.actions.icon"="bell"
LABEL "com.github.actions.color"="green"
LABEL "com.github.actions.name"="Slack Notify"
LABEL "com.github.actions.description"="This action will send notification to Slack"
LABEL "org.opencontainers.image.source"="https://github.com/DataMa-Solutions/action-slack-notify"

RUN pip3 install requests
COPY slack.py /slack
RUN chmod +x /slack

ENTRYPOINT ["/slack"]
