# Dockerfile for Python Application  
FROM python:3.9-slim  

# Set the working directory in the container  
WORKDIR /app  

# Copy the requirements file if you have one  
# If you have a requirements.txt, uncomment these lines  
# COPY requirements.txt .  
# RUN pip install --no-cache-dir -r requirements.txt  

# Copy all your application files into the Docker image  
COPY . .  

# Install necessary packages for your application  
RUN pip install requests beautifulsoup4 mysql-connector-python  

# Command to run the application  
CMD ["python", "analyze_listings.py"]  