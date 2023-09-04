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

# Set database environment variables
ENV DB_ENGINE=django.db.backends.postgresql
ENV DB_NAME=scutes
# Is POSTGRES_USER in k8s
ENV DB_USER=''
# Is POSTGRES_PASSWORD in k8s
ENV DB_PASSWORD=''
# Is DB_HOST in k8s
ENV DB_HOST=''
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
