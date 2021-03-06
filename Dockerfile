# Use an official Python runtime as a parent image
FROM python:3.7
LABEL maintainer="hello@wagtail.io"

# Set arguments

ARG DJANGO_ENV=dev

# Set environment varibles
ENV PYTHONUNBUFFERED 1
ENV DJANGO_ENV ${DJANGO_ENV}

COPY ./requirements.txt /code/requirements.txt
RUN pip install --upgrade pip
# Install any needed packages specified in requirements.txt
RUN pip install -r /code/requirements.txt
RUN pip install gunicorn

# Copy the current directory contents into the container at /code/
COPY . /code/
# Set the working directory to /code/
WORKDIR /code/

RUN useradd wagtail
RUN chown -R wagtail /code
USER wagtail

EXPOSE 8000
CMD python manage.py migrate
CMD python manage.py collectstatic --noinput
CMD exec gunicorn simpelsite.wsgi:application --bind 0.0.0.0:8000 --workers 3