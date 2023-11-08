FROM python:3.11.3

WORKDIR /root

RUN apt-get update && \
  apt-get install libxml2 libxslt1-dev && \
  mkdir tp.dba.python

COPY ./ /root/tp.dba.python

CMD /bin/bash
