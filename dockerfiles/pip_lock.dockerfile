FROM python:3.10

WORKDIR /tmp/install
RUN pip install pip-tools
