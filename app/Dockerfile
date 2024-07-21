FROM python:3.10

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file into the container at /app
COPY requirements.txt .

# Install any dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the working directory contents into the container at /app
COPY . .

# Ensure the start_services.sh script has executable permissions
RUN chmod +x start_services.sh

# Expose port 5055 for Rasa actions server
EXPOSE 5055

# Expose port 5005 for Rasa server
EXPOSE 5005

# Run a shell script to start the services
CMD ["./start_services.sh"]