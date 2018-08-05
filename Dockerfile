# Use an official Python runtime as a parent image
FROM python:3.6

#RUN echo DOCKER_HOST=127.0.0.1:2375

ARG DOCKER_HOST=${DOCKER_HOST:-""}
ENV DOCKER_HOST=${DOCKER_HOST}

#CMD echo "DOCKER_HOST is ${DOCKER_HOST}"

# Create the app dir
RUN mkdir -p /app

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
ADD . /app

# Remove old piston stack
RUN curl https://raw.githubusercontent.com/steemit/steem-python/master/scripts/nuke_legacy.sh | sh

# Upgrade pip
RUN pip install --upgrade pip

# Compile the steem library
RUN pip install -U git+git://github.com/steemit/steem-python

# Install the library for steem
RUN pip install -U steem

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt
#RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variable
ENV NAME World

# Run app.py when the container launches
CMD ["python", "app.py"]

