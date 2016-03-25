# start from base
FROM ubuntu:14.04
MAINTAINER Stephen Perl

# install system-wide deps for python and node
RUN apt-get -yqq update
RUN apt-get -yqq install python-pip python-dev

# copy our application code
ADD . /opt/flask-app
WORKDIR /opt/flask-app

# fetch app specific deps
RUN pip install -r requirements.txt

# expose port
EXPOSE 5000

# start app
CMD [ "python", "./app.py" ]