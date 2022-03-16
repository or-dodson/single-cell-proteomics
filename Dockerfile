FROM ubuntu:22.04

LABEL maintainer="Evan Dodson or.dodson.evan@gmail.com"

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get full-upgrade -y && apt-get install -y wget zlib1g-dev vim

WORKDIR /root

#RUN apt-get install -y python3.9-full

#RUN wget https://bootstrap.pypa.io/get-pip.py && python3 ./get-pip.py


RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-aarch64.sh && chmod +x ./Miniconda3-latest-Linux-aarch64.sh && ./Miniconda3-latest-Linux-aarch64.sh -b -p $HOME/miniconda

RUN ~/miniconda/bin/activate && echo "PATH=$HOME/miniconda/bin:$PATH" >> ~/.bashrc

RUN python3 -m pip install pgmpy numpy pandas matplotlib pyteomics networkx ppx

RUN conda install -c conda-forge metamorpheus
