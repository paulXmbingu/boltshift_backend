# Use the official Python image as a parent image
FROM python:3.9

# Set environment variables (change as needed)
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Create and set the working directory
RUN mkdir /app
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt /app/

# Install dependencies from requirements.txt
RUN pip install -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app/

# Expose the port that the Django application will run on
EXPOSE 8000

# Run the Django application using Gunicorn
CMD ["gunicorn", "boltshift.wsgi:application", "--bind", "0.0.0.0:8000"]
