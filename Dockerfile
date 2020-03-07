# Use an official Python runtime as a parent image
FROM python:3.7
LABEL maintainer="hello@wagtail.io"

# Build Args
# Set environment varibles
ENV PYTHONUNBUFFERED 1

# Copy the current directory contents into the container at /code/

RUN mkdir /code
RUN mkdir /code/staticfiles
COPY . /code/

# Set the working directory to /code/
WORKDIR /code/
RUN pwd

# Install any needed packages specified in requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install gunicorn

EXPOSE 8000
CMD exec gunicorn intradarmajaya.wsgi:application --bind 0.0.0.0:8000 --workers 3