# Use official Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy your app files
COPY . /app

# Install dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir flask nltk pandas scikit-learn

# Download NLTK data
RUN python -m nltk.downloader all

# Expose Flask port
EXPOSE 5000

# Run the app
CMD ["python", "app.py"]
