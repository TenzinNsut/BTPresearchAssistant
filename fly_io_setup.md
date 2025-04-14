# Deploying to Fly.io

This guide will help you deploy your Research Assistant application to Fly.io's free tier.

## Prerequisites

- A Fly.io account
- The Fly CLI installed
- Git installed

## Step 1: Install the Fly CLI

Install the Fly.io CLI:

**Linux/Mac**:
```bash
curl -L https://fly.io/install.sh | sh
```

**Windows (with PowerShell)**:
```powershell
iwr https://fly.io/install.ps1 -useb | iex
```

## Step 2: Sign Up and Log In

If you don't have an account:
```bash
fly auth signup
```

If you already have an account:
```bash
fly auth login
```

## Step 3: Prepare Your Application

1. Make sure you have the `Dockerfile` in your project root.
2. Ensure your `.gitignore` includes `.env` to avoid committing sensitive information.

## Step 4: Launch Your Application

From your project directory, run:
```bash
fly launch
```

Follow the prompts:
- Enter a unique app name
- Choose a region close to your users
- Set up a PostgreSQL database if needed (optional)

## Step 5: Set Environment Variables

Set the environment variables required for your application:
```bash
fly secrets set HUGGINGFACE_API_KEY="your_huggingface_api_key"
fly secrets set PINECONE_API_KEY="your_pinecone_api_key"
fly secrets set PINECONE_ENVIRONMENT="your_pinecone_environment"
```

## Step 6: Deploy Your Application

Deploy your application with:
```bash
fly deploy
```

## Step 7: Open Your Application

Once deployment is complete, open your app in a web browser:
```bash
fly open
```

Your app will be available at `https://your-app-name.fly.dev`.

## Additional Configuration

### 1. Scale Your Application

To adjust the resources for your app:
```bash
fly scale memory 1024 # Set memory to 1GB
fly scale cpu 1       # Set CPU to 1 core
```

### 2. Set Up a Custom Domain

```bash
fly certs create your-domain.com
```

Update your DNS settings to point to your Fly.io app.

### 3. Monitoring and Logs

View application logs:
```bash
fly logs
```

Monitor your application:
```bash
fly status
```

### 4. Storage Configuration

For persistent storage (for uploads):
```bash
fly volumes create research_uploads --size 1 --region your-region
```

Then update your Dockerfile to mount this volume to your `/app/uploads` directory.

## Troubleshooting

If you encounter issues:

1. Check application logs with `fly logs`
2. Ensure all environment variables are set with `fly secrets list`
3. Verify your Dockerfile is correct
4. For persistent storage issues, check volume mounts with `fly volumes list`

## Free Tier Limitations

Fly.io's free tier includes:
- 3 shared-cpu-1x 256MB VMs
- 3GB persistent volume storage
- 160GB outbound data transfer

Be mindful of these limitations to avoid unexpected charges. 