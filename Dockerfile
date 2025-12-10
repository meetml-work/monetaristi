# Base image
# Base image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install system dependencies for PostgreSQL support
RUN apt-get update && apt-get install -y build-essential libpq-dev && apt-get clean

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy the entire Django project
COPY . /app/

# Collect static files for production
RUN python manage.py collectstatic --noinput

# Expose port
EXPOSE 8000

# Run migrations then start gunicorn
CMD python manage.py migrate && gunicorn blog.wsgi:application --bind 0.0.0.0:$PORT