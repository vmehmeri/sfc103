FROM debian:latest
RUN apt-get -y update
RUN apt-get install -y git python python-pip
RUN mkdir /scripts
ADD ../setup.py /scripts/setup.py
ADD ../setup1.py /scripts/setup1.py
ADD ../setup2.py /scripts/setup2.py
