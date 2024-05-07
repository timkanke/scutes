# Pull base image
FROM python:3.11.4-slim

# Set environment variables
ENV PIP_DISABLE_PIP_VERSION_CHECK=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /opt/scutes

# Install dependencies
COPY ./requirements.txt .
RUN apt-get update && apt-get install -y xmlsec1 libssl-dev libsasl2-dev git
RUN pip install -r requirements.txt

# Copy project
COPY src ./src
COPY pyproject.toml .

RUN python src/manage.py collectstatic
CMD python src/manage.py migrate && runserver 0.0.0.0:15000
