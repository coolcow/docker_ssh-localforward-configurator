FROM python:latest

MAINTAINER Jean-Michel Ruiz "mail@coolcow.org"

COPY servicesToSshConf.py /tmp

ENTRYPOINT ["/tmp/servicesToSshConf.py"]
