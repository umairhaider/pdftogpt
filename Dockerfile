# Uses the official Python base image
FROM python:3.9

# Sets the working directory in the container
WORKDIR /app

# Copies the requirements file to the working directory
COPY requirements.txt .

# Installs the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copies the entire project to the working directory
COPY . .

# Exposes the port that the FastAPI application will listen on
EXPOSE 8000

# Starts the FastAPI application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]