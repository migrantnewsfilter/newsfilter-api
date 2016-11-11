FROM python:2-onbuild

# RUN echo "deb http://ftp.debian.org/debian jessie-backports main" > /etc/apt/sources.list.d/backports.list
# RUN sudo apt-get update
# RUN sudo apt-get install certbot -t jessie-backports

ADD . /newsfilter
RUN pip install -r /newsfilter/requirements.txt

EXPOSE 5000

WORKDIR /newsfilter

CMD [ "python", "__main__.py" ]
