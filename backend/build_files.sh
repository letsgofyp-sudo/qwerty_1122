#!/bin/bash

# Install Python dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --noinput

# Make migrations and apply them
python manage.py makemigrations
python manage.py migrate

# Create a build directory for Vercel
mkdir -p vercel_build
cp -r ./* vercel_build/ 2>/dev/null || :
# The build output directory is .vercel_build_output by default for Vercel
# We'll copy our files there to be deployed
mkdir -p .vercel_build_output
cp -r vercel_build/* .vercel_build_output/ 2>/dev/null || :
