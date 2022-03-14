# Base image for the application
FROM python:3.7
# Project maintainer information
LABEL maintainer="Mokit Hossain"

# Application working directory
WORKDIR /app
# Copy the current directory context to the container
ADD . .

# Install application related library
RUN pip install -r requirements.txt

# Application expose port number
EXPOSE 50000

# Application executable command
CMD ["python", "app.py"]