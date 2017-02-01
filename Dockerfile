FROM andrewosh/binder-base

MAINTAINER Robert Gieseke <robert.gieseke@pik-potsdam.de>

USER root

RUN apt-get update && apt-get install -y libboost-filesystem-dev libboost-system-dev --no-install-recommends && apt-get clean

USER main

RUN git clone https://github.com/swillner/pyhector.git /home/main/pyhector --recursive

RUN cd /home/main/pyhector && python setup.py develop --user && mv libpyhector.so /home/main/notebooks/ && cp /home/main/notebooks/examples/* .
