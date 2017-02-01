FROM andrewosh/binder-base

MAINTAINER Robert Gieseke <robert.gieseke@pik-potsdam.de>

USER root

RUN apt-get update && apt-get install -y libboost-filesystem-dev libboost-system-dev --no-install-recommends && apt-get clean

COPY . /home/main/pyhector/

RUN chown -R main:main /home/main/pyhector

USER main

RUN cd /home/main/pyhector && pip install .
