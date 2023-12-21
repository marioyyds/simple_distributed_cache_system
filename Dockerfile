FROM ubuntu:20.04
COPY . .
# modify unbuntu deb source to get python3 and pip fast
RUN mv sources.list /etc/apt/sources.list
RUN apt-get update
RUN apt-get install python3 -y
RUN apt-get install python3-pip -y
# use tsinghua mirror to download python3 modules fast
RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt