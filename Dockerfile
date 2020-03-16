# Use an official Python runtime as a parent image
FROM python:3.7
LABEL maintainer="sasri.project@gmail.com"

# Set arguments

ARG database_url

# Set environment varibles
ENV PYTHONUNBUFFERED 1
ENV DJANGO_ENV production

RUN pip install --upgrade pip
RUN pip install gunicorn pipenv

# Copy the current directory contents into the container at /code/
COPY . /code/

# Set the working directory to /code/
WORKDIR /code/

# Install any needed packages specified in requirements.txt
RUN pipenv install --skip-lock

RUN useradd wagtail
RUN chown -R wagtail /code
USER wagtail

EXPOSE 8000
CMD python manage.py collectstatic --noinput
CMD exec gunicorn simpelsite.wsgi:application --bind 0.0.0.0:8000 --workers 3