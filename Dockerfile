FROM ubuntu:20.04
RUN apt-get update
RUN apt-get install python3 -y
RUN python3
COPY ./requirements.txt ./requirements.txt
RUN apt-get install python3-pip -y
RUN pip install -r requirements.txt
COPY *.py .
# RUN apt-get install curl -y