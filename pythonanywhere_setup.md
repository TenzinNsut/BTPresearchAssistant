# Deploying to PythonAnywhere

This guide will help you deploy your Research Assistant application to PythonAnywhere's free tier.

## Step 1: Sign Up for PythonAnywhere

1. Go to [PythonAnywhere](https://www.pythonanywhere.com/) and sign up for a free account
2. Once logged in, go to the Dashboard

## Step 2: Set Up a Web App

1. Click on the "Web" tab in the top navigation
2. Click "Add a new web app"
3. Select the Python version (3.11)
4. Select "Flask" as your framework
5. Enter the path to your Flask app (`/home/yourusername/research-assistant/main.py`)

## Step 3: Clone Your Repository

1. Go to the "Consoles" tab and start a new Bash console
2. Clone your repository:
   ```bash
   git clone https://github.com/yourusername/research-assistant.git
   ```

## Step 4: Set Up Virtual Environment

1. Still in the Bash console, create and activate a virtual environment:
   ```bash
   cd research-assistant
   python -m venv venv
   source venv/bin/activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Step 5: Run the Build Script

1. Make the build script executable and run it:
   ```bash
   chmod +x build.sh
   ./build.sh
   ```

## Step 6: Configure WSGI File

1. Go to the "Web" tab
2. Click on the WSGI configuration file link (e.g., `/var/www/yourusername_pythonanywhere_com_wsgi.py`)
3. Replace the content with:

```python
import sys
import os

# Add your project directory to the sys.path
path = '/home/yourusername/research-assistant'
if path not in sys.path:
    sys.path.insert(0, path)

# Import your app and create dotenv
os.environ['HUGGINGFACE_API_KEY'] = 'your_huggingface_api_key'
os.environ['PINECONE_API_KEY'] = 'your_pinecone_api_key'
os.environ['PINECONE_ENVIRONMENT'] = 'your_pinecone_environment'

from main import app as application
```

4. Save the file

## Step 7: Set Up Static Files

1. Go to the "Web" tab
2. In the "Static files" section, add:
   - URL: `/static/`
   - Directory: `/home/yourusername/research-assistant/static`

## Step 8: Reload Your Web App

1. Go to the "Web" tab
2. Click the "Reload" button for your web app

## Step 9: Access Your Application

Your application should now be available at:
```
https://yourusername.pythonanywhere.com
```

## Troubleshooting

If you encounter any issues:

1. Check the error logs in the "Web" tab
2. Make sure all directories have proper permissions
3. Ensure your environment variables are set correctly
4. Check if all dependencies were installed properly

Remember to keep your API keys secure and never commit them to your repository. 