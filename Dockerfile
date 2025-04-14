FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p static uploads templates
RUN chmod -R 755 static uploads templates

# Run the build script to generate static files
RUN chmod +x ./build.sh
RUN ./build.sh

# Expose port
EXPOSE 8080

# Start the app with gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "main:app"] 