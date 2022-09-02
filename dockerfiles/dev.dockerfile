FROM python:3.10

WORKDIR /tmp/install
COPY ./requirements/requirements.txt ./requirements.txt
RUN pip install -r requirements.txt
