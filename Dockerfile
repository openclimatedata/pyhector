FROM andrewosh/binder-base

MAINTAINER Robert Gieseke <robert.gieseke@pik-potsdam.de>

USER root

RUN apt-get update && \
    apt-get install -y libboost-filesystem-dev libboost-system-dev --no-install-recommends && \
    apt-get clean

USER main

RUN cd / && \
    rm -r $HOME/notebooks && \
    git clone https://github.com/swillner/pyhector.git $HOME/notebooks --recursive && \
    cd $HOME/notebooks && \
    python setup.py develop --user && \
    mv examples/pyhector.ipynb index.ipynb

ENV LD_LIBRARY_PATH=/usr/lib/x86_64-linux-gnu/:$LD_LIBRARY_PATH
