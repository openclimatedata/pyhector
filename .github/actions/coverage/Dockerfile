ARG PYTHON_VERSION=latest
FROM python:$PYTHON_VERSION

LABEL "com.github.actions.name"="Run for Python"
LABEL "com.github.actions.description"="Run command in a Python-supporting environment"
LABEL "com.github.actions.icon"="command"
LABEL "com.github.actions.color"="blue"

RUN apt-get update; apt-get install -y libboost-system-dev libboost-filesystem-dev; apt-get clean
RUN pip install --upgrade pip
RUN pip install coverage pytest pytest-cov

ADD entrypoint.sh /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
