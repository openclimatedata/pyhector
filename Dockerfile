FROM jupyter/scipy-notebook:2022-01-12

MAINTAINER Robert Gieseke <rob.g@web.de>

USER root

RUN apt-get update && \
    apt-get install -y libboost-filesystem-dev libboost-system-dev --no-install-recommends && \
    apt-get clean

RUN pip install --upgrade pip
RUN pip install pyhector

COPY . ${HOME}
USER root
RUN chown -R ${NB_UID} ${HOME}
USER ${NB_USER}
