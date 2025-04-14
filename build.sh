#!/bin/bash

# Create necessary directories if they don't exist
mkdir -p static
mkdir -p templates
mkdir -p uploads

# Ensure permissions are set correctly
chmod -R 755 static
chmod -R 755 templates
chmod -R 755 uploads

# Verify static files exist
if [ ! -f "static/styles.css" ]; then
  echo "styles.css not found in static folder, checking for alternative locations..."
  
  # Check if it might be in 'Static' folder
  if [ -d "Static" ] && [ -f "Static/styles.css" ]; then
    echo "Found styles.css in Static folder, copying to static folder..."
    cp Static/styles.css static/styles.css
    chmod 644 static/styles.css
  fi
fi

if [ ! -f "static/homeStyle.css" ]; then
  echo "homeStyle.css not found in static folder, checking for alternative locations..."
  
  # Check if it might be in 'Static' folder
  if [ -d "Static" ] && [ -f "Static/homeStyle.css" ]; then
    echo "Found homeStyle.css in Static folder, copying to static folder..."
    cp Static/homeStyle.css static/homeStyle.css
    chmod 644 static/homeStyle.css
  fi
fi

# List contents of static directory to verify
echo "Contents of static directory:"
ls -la static/

# Link static files to the correct location if needed
if [ ! -d "static" ]; then
  echo "Static folder not found, creating symbolic link..."
  ln -s Static static
fi

# Verify template files
if [ ! -f "templates/index.html" ] && [ -f "templates/Index.html" ]; then
  echo "Creating lowercase index.html from Index.html..."
  cp templates/Index.html templates/index.html
fi

echo "Build script completed successfully!" 