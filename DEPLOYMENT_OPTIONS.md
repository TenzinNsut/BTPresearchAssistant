# Free Deployment Options for Your Research Assistant App

Here are several free hosting options that would work well for your Flask application:

## 1. PythonAnywhere

**Pros:**
- Free tier available with 500MB disk space
- Native support for Python web applications (Flask, Django)
- No credit card required
- Custom domain available even on free tier
- Easy deployment process (Git or manual upload)

**Cons:**
- Limited CPU time on free tier
- No HTTPS on free tier custom domains
- Free tier runs only during active use

**Deployment Steps:**
1. Create an account at [PythonAnywhere](https://www.pythonanywhere.com/)
2. Create a Web App and select Flask
3. Clone your Git repository or upload your files
4. Set up a virtual environment with your dependencies
5. Configure your WSGI file
6. Set environment variables in the dashboard

## 2. Fly.io

**Pros:**
- Generous free tier (3 shared-cpu VMs, 3GB RAM, 160GB storage total)
- Global deployment
- Free SSL certificates
- Persistent storage available
- Full Docker support

**Cons:**
- Requires credit card for verification (but won't charge unless you exceed free tier)
- Slightly more complex setup than PythonAnywhere

**Deployment Steps:**
1. Install Fly CLI: `curl -L https://fly.io/install.sh | sh`
2. Sign up: `flyctl auth signup`
3. Create a Dockerfile in your project
4. Deploy: `flyctl launch`
5. Set environment variables: `flyctl secrets set KEY=VALUE`

## 3. Railway

**Pros:**
- Free tier with $5 credit monthly
- Easy GitHub integration
- Automatic deployments
- Custom domains with SSL
- Built-in database options

**Cons:**
- Time limit on free tier (limited runtime hours)
- Credit card required for verification

**Deployment Steps:**
1. Create an account at [Railway](https://railway.app/)
2. Connect your GitHub repository
3. Add environment variables in the dashboard
4. Deploy from GitHub
5. Optional: Add a custom domain

## 4. Replit

**Pros:**
- Completely free
- No credit card required
- Integrated development environment
- Easy to share and collaborate
- Good for educational purposes

**Cons:**
- Limited resources
- Apps sleep after inactivity (slower startup)
- Not ideal for production use

**Deployment Steps:**
1. Create an account at [Replit](https://replit.com/)
2. Create a new Repl with Python template
3. Import from GitHub or upload files
4. Set up environment variables
5. Run your app
6. Replit automatically provides a public URL

## 5. Oracle Cloud Free Tier

**Pros:**
- Always free resources
- 2 AMD VMs with 1 GB RAM each
- 200 GB total storage
- Complete control (like having your own server)
- No auto-expiration

**Cons:**
- More complex setup
- Requires server administration knowledge
- Credit card required for verification

**Deployment Steps:**
1. Sign up for Oracle Cloud Free Tier
2. Create a VM instance
3. SSH into your VM
4. Install dependencies and clone your repository
5. Set up NGINX as a reverse proxy
6. Configure environment variables
7. Use systemd to keep your application running

## Recommendation

For your Research Assistant app, I recommend:

1. **PythonAnywhere** if you want the easiest setup and don't expect heavy usage
2. **Fly.io** if you want better performance and are comfortable with Docker
3. **Oracle Cloud Free Tier** if you want full control and are comfortable with server administration

Remember to secure your API keys as environment variables and not commit them to your repository. 