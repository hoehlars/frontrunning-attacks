FROM python:3.9-slim

# Create and set the working directory

ENV NODE_URL=https://orbital-cosmopolitan-moon.quiknode.pro/6f78ef5955370adc5f0a37f2e25e95cdd723119f/
ENV MONGO_URI=mongodb+srv://larshoehener:4JYDS9UYJ5VOZvgR@cluster0.sd1cyte.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0
ENV MONGO_DB=liveTransactionsEthDb
ENV MONGO_COLLECTION=liveTransactionsClassification

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