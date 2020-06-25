FROM python:3.8-slim-buster

# The enviroment variable ensures that the python output is set straight
# to the terminal with out buffering it first
ENV PYTHONUNBUFFERED 1

#install required infra modules
RUN apt-get install -y

# create root directory for our project in the container
RUN mkdir /usr/src/ccp-backend-brain

# set work directory to /usr/src/ccp-backend-brain
WORKDIR /usr/src/ccp-backend-brain

# Copy requirement.txt & Install any needed packages specified in requirements.txt
COPY requirements.txt /usr/src/ccp-backend-brain/
RUN pip install -r requirements.txt

# Copy the current directory contents into the container at /music_service
ADD . /usr/src/ccp-backend-brain/
