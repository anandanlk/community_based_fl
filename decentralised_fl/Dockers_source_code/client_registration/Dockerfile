FROM python:3.8-slim-buster

WORKDIR /register
ADD ./requirements.txt /register/requirements.txt
RUN --mount=type=cache,target=/root/.cache/pip3 pip3 install -r requirements.txt --no-cache-dir

ARG COMMUNICATION_IP=default_value
ENV COMMUNICATION_IP ${COMMUNICATION_IP}


RUN echo $COMMUNICATION_IP
COPY . .

CMD python register.py $COMMUNICATION_IP