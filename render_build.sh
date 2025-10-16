#!/usr/bin/env bash
# Exit immediately on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Run database migrations automatically
python manage.py migrate

# Collect static files (optional)
python manage.py collectstatic --no-input
