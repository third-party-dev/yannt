FROM debian:13-slim

RUN apt-get update && apt-get install -y \
    python3.13 python3-pip python3-venv git neovim curl

ARG VENV_PATH=/opt/ml-venv

RUN python3 -m venv $VENV_PATH \
    && $VENV_PATH/bin/pip install --upgrade pip setuptools wheel \
    && chmod -R a+rX $VENV_PATH

ENV PATH="$VENV_PATH/bin:$PATH"

RUN pip install torch torchaudio torchvision --index-url https://download.pytorch.org/whl/cpu
RUN pip install transformers
RUN pip install numpy
RUN pip install protobuf
RUN pip install pytest

# if dev
#RUN pip install -e /opt/yannt
#RUN pip install -e /opt/pparse
# if deploy
#RUN pip install /opt/wheels/yannt.whl
#RUN pip install /opt/wheels/pparse.whl


#ADD tester.sh /
#WORKDIR /host
#ENTRYPOINT ["/tester.sh"]