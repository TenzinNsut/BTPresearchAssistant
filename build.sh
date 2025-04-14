#!/bin/bash

# Create necessary directories if they don't exist
mkdir -p static
mkdir -p templates
mkdir -p uploads

# Ensure permissions are set correctly
chmod -R 755 static
chmod -R 755 templates
chmod -R 755 uploads

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