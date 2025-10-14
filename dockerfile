# Use official Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy your app files
COPY . /app

# Install dependencies
RUN pip install --upgrade pip
RUN pip install streamlit nltk scikit-learn

# Download NLTK data
RUN python -m nltk.downloader stopwords punkt

# Expose Streamlit port
EXPOSE 8501

# Run the app
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
