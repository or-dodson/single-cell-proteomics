FROM ubuntu:22.04

LABEL maintainer="Evan Dodson or.dodson.evan@gmail.com"

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get full-upgrade -y && apt-get install -y wget zlib1g-dev vim git zip libssl1.1 libicu70

WORKDIR /root

#RUN apt-get install -y python3.9-full

#RUN wget https://bootstrap.pypa.io/get-pip.py && python3 ./get-pip.py


RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh && chmod +x ./Miniconda3-latest-Linux-x86_64.sh && ./Miniconda3-latest-Linux-x86_64.sh -b -p $HOME/miniconda

RUN ~/miniconda/bin/activate && echo "PATH=$HOME/miniconda/bin:$HOME/.dotnet:$PATH" >> ~/.bashrc

RUN ~/miniconda/bin/python3 -m pip install pgmpy numpy pandas matplotlib pyteomics networkx ppx

#RUN ~/miniconda/bin/conda install -c conda-forge metamorpheus -y

RUN ~/miniconda/bin/conda install jupyterlab ipywidgets


#RUN ~/miniconda/bin/conda install ipywidgets

RUN wget https://dot.net/v1/dotnet-install.sh

RUN chmod +x ./dotnet-install.sh && ./dotnet-install.sh -c 5.0

#required for metamorpheus for some reason
RUN wget https://github.com/smith-chem-wisc/MetaMorpheus/releases/download/0.0.320/MetaMorpheus_CommandLine.zip
RUN unzip MetaMorpheus_CommandLine.zip -d Metamorpheus
#for forcing a clone on every build
RUN git clone https://github.com/or-dodson/single-cell-proteomics.git
