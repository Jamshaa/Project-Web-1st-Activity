# Use a lightweight Python image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /RecipeSearch

# Copy Poetry configuration files
COPY cooking/RecipeSearch/pyproject.toml poetry.lock* ./

# Install Poetry
RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-root --no-interaction --no-ansi

# Ensure Gunicorn is installed
RUN poetry run pip install gunicorn

# Copy the entire RecipeSearch project into the container
COPY cooking/RecipeSearch/ /RecipeSearch/

# Expose the port Django will run on
EXPOSE 8000

RUN python manage.py collectstatic --noinput

# Run the application using Gunicorn
CMD ["poetry", "run", "gunicorn", "RecipeSearch.wsgi:application", "--bind", "0.0.0.0:8000"]
