FROM python:3.9-slim

# Create and set the working directory

WORKDIR /app

# Copy only the requirements file first to leverage Docker caching
COPY requirements.txt .

# Install dependencies
RUN pip install --upgrade pip setuptools
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire application code
COPY . .

# Specify the command to run on container start
CMD ["python", "transaction_listener.py"]