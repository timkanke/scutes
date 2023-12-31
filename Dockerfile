# Pull base image
FROM python:3.11.4-slim

# Set environment variables
ENV PIP_DISABLE_PIP_VERSION_CHECK=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DEBUG=off
ENV ALLOWED_HOSTS=localhost,127.0.0.1,host.docker.internal
ENV LOGGING_LEVEL=INFO
# DJANGO_LOG_LEVEL=DEBUG setting is very verbose as it includes all database queries.
ENV DJANGO_LOG_LEVEL=INFO

ENV MEDIA_URL='/media/'
ENV MEDIA_ROOT='/media'

# Set database environment variables
ENV DB_ENGINE=django.db.backends.postgresql
ENV DB_NAME=scutes
# Was POSTGRES_USER in k8s, now DB_USER
# ENV DB_USER=''
# Was POSTGRES_PASSWORD in k8s, now DB_PASSWORD
# ENV DB_PASSWORD=''
# ENV DB_HOST=''
ENV DB_PORT=5432

# Set work directory
WORKDIR /scutes

# Install dependencies
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# Copy project
COPY src ./src
COPY pyproject.toml .

CMD python src/manage.py runserver 0.0.0.0:8000
