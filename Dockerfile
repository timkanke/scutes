# Pull base image
FROM python:3.11.4-slim

# Set environment variables
ENV PIP_DISABLE_PIP_VERSION_CHECK=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /opt/scutes

# Install dependencies
RUN apt-get update && apt-get install -y xmlsec1 libssl-dev libsasl2-dev git
COPY pyproject.toml .
RUN pip install -e .

# Copy project
COPY src ./src

# Commands to run migration and start the server
RUN python src/manage.py collectstatic --noinput
CMD python src/manage.py migrate && runserver 0.0.0.0:15000