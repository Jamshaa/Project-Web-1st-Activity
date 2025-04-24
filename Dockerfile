# Use a lightweight Python image
FROM python:3.11-slim

# Install system dependencies required for Pillow and build tools
RUN apt-get update && apt-get install -y \
    libjpeg-dev \
    zlib1g-dev \
    libpng-dev \
    gcc \
    gfortran \
    libopenblas-dev \
    liblapack-dev \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory inside the container
WORKDIR /RecipeSearch

# Copy requirements file
COPY cooking/requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir numpy==1.24.3 && \
    pip install --no-cache-dir -r requirements.txt

# Install Pillow
RUN pip install Pillow

# Ensure Gunicorn is installed
RUN pip install gunicorn

# Create necessary directories
RUN mkdir -p /RecipeSearch/static /RecipeSearch/staticfiles /RecipeSearch/media

# Copy the entire RecipeSearch project into the container
COPY cooking/RecipeSearch/ /RecipeSearch/

# Expose the port Django will run on
EXPOSE 8000

# Run collectstatic with --noinput flag
RUN python manage.py collectstatic --noinput || true

# Run the application using Gunicorn
CMD ["gunicorn", "RecipeSearch.wsgi:application", "--bind", "0.0.0.0:8000"]
