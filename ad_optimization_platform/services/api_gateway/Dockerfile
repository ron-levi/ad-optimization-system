# Use official Python image as base
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies needed for Poetry & compiling dependencies
RUN apt-get update && apt-get install -y \
    curl build-essential gcc python3-dev liblz4-dev \
    && rm -rf /var/lib/apt/lists/*

# Manually install Poetry using pip (instead of the installer script)
RUN pip install --upgrade pip && pip install poetry==2.1.1    

# Set Poetry environment variables (prevents Poetry from creating a virtualenv inside the container)
ENV PATH="/root/.local/bin:$PATH" \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1

# Copy only dependency files first (for better caching)
COPY pyproject.toml poetry.lock ./

# Install dependencies using Poetry
RUN poetry install --only main --no-root

# Copy the rest of the application
COPY . .

# Expose the application port
EXPOSE 8000

# Set default command
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]