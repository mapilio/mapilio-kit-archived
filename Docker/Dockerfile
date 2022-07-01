FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /mapilio_kit

RUN apt update -y && apt install -y python3 python3-pip git && apt install -y --no-install-recommends ffmpeg
RUN apt install exiftool -y
RUN apt install libjpeg-turbo8-dev

RUN python3 -m pip install --upgrade git+https://github.com/mapilio/mapilio-kit@gopromax_docker

RUN set -e && mkdir -p bin && mkdir -p dependencies

RUN git -C dependencies  clone https://github.com/mcvarer/max2sphere-batch

RUN make -C dependencies/max2sphere-batch -j

RUN cp dependencies/max2sphere-batch/MAX2spherebatch bin/

RUN mapilio_kit --version