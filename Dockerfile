FROM andrewosh/binder-base

MAINTAINER Robert Gieseke <robert.gieseke@pik-potsdam.de>

USER root

RUN apt-get update && \
    apt-get install -y libboost-filesystem-dev libboost-system-dev --no-install-recommends && \
    apt-get clean

USER main

RUN cd / && \
    rm -r $HOME/notebooks && \
    git clone https://github.com/openclimatedata/pyhector.git $HOME/notebooks --recursive && \
    cd $HOME/notebooks && \
    python setup.py develop --user && \
    ln -sf /usr/lib/x86_64-linux-gnu/libstdc++.so.6.0.20 /home/main/anaconda2/envs/python3/lib/libstdc++.so.6
