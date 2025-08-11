# --- Base Image ---
# We use the official Python 3.12 slim image as a base.
# "slim" is a smaller version, which is good for production.
FROM python:3.12-slim

# --- Environment Variables ---
# Set environment variables to prevent Python from writing .pyc files
# and to ensure output is sent directly to the terminal without buffering.
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# --- Working Directory ---
# Set the working directory inside the container.
# All subsequent commands (RUN, COPY, CMD) will be executed from this path.
WORKDIR /app

# --- Install System Dependencies ---
# Update the package list and install dependencies needed for libraries like psycopg2.
# We also clean up the apt cache to keep the image size small.
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc libpq-dev gdal-bin libgdal-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# --- Install Python Dependencies ---
# First, copy only the requirements file.
# This takes advantage of Docker's layer caching. If the requirements don't change,
# Docker won't re-install them every time, speeding up the build process.
COPY ./src/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# --- Copy Project Code ---
# Copy the rest of the application's source code into the container.
COPY ./src /app

# --- Expose Port ---
# Inform Docker that the container listens on port 8000 at runtime.
# This does not actually publish the port.
EXPOSE 8000

# --- Default Command ---
# The command to run when the container starts.
# We will use Gunicorn as our production web server.
# For now, we can add a placeholder or a command for development.
# We will refine this later. For now, we'll run the Django development server.
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]