FROM andrewosh/binder-base

MAINTAINER Robert Gieseke <robert.gieseke@pik-potsdam.de>

USER root

# Add dependencies
RUN apt-get update
RUN apt-get install -y libboost-filesystem-dev libboost-system-dev && apt-get clean

USER main

RUN /bin/bash -c "source activate python3"
RUN python setup.py install
