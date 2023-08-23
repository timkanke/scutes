# Pull base image
FROM python:3.11.4-slim

# Set environment variables
ENV PIP_DISABLE_PIP_VERSION_CHECK=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DEBUG=off
ENV ALLOWED_HOSTS=localhost,127.0.0.1,host.docker.internal

# Set work directory
WORKDIR /scutes

# Install dependencies
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# Copy project
COPY src ./src
COPY pyproject.toml .

CMD python src/manage.py runserver 0.0.0.0:8000
