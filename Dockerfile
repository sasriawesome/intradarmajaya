# Use an official Python runtime as a parent image
FROM python:3.7
LABEL maintainer="hello@wagtail.io"

# Set environment varibles
ENV PYTHONUNBUFFERED 1
ENV DJANGO_ENV dev
ENV DATABASE_URL=$DATABASE_URL
ENV SECRET_KEY=$SECRET_KEY
ENV EMAIL_HOST=$EMAIL_HOST
ENV EMAIL_PORT=$EMAIL_PORT
ENV EMAIL_HOST_USER=$EMAIL_HOST_USER
ENV EMAIL_HOST_PASSWORD=$EMAIL_HOST_PASSWORD
ENV AWS_S3_CUSTOM_DOMAIN=$AWS_S3_CUSTOM_DOMAIN
ENV AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID
ENV AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY
ENV AWS_STORAGE_BUCKET_NAME=$AWS_STORAGE_BUCKET_NAME
ENV AWS_S3_ENDPOINT_URL=$AWS_S3_ENDPOINT_URL
ENV AWS_LOCATION=$AWS_LOCATION
ENV DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE

COPY ./requirements.txt /code/requirements.txt
RUN pip install --upgrade pip
# Install any needed packages specified in requirements.txt
RUN pip install -r /code/requirements.txt
RUN pip install gunicorn

# Copy the current directory contents into the container at /code/
COPY . /code/
# Set the working directory to /code/
WORKDIR /code/

RUN python manage.py migrate
RUN python manage.py collectstatic --noinput

RUN useradd wagtail
RUN chown -R wagtail /code

USER wagtail

EXPOSE 8000
CMD exec gunicorn intradarmajaya.wsgi:application --bind 0.0.0.0:8000 --workers 3