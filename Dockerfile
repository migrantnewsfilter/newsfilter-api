FROM python:2-onbuild

ADD . /newsfilter
RUN pip install -r /newsfilter/requirements.txt

EXPOSE 5000

WORKDIR /newsfilter

CMD [ "python", "__main__.py" ]
