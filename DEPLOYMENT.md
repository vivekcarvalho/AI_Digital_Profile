# Deployment Guide

Complete guide for deploying the AI-Powered Digital Profile Website to production.

## Table of Contents

1. [Streamlit Cloud (Recommended)](#streamlit-cloud)
2. [Heroku](#heroku)
3. [AWS EC2](#aws-ec2)
4. [Google Cloud Run](#google-cloud-run)
5. [Environment Variables](#environment-variables)
6. [Security Best Practices](#security)

---

## Streamlit Cloud (Recommended)

**Best for**: Quick deployment, free hosting, easy updates

### Prerequisites
- GitHub account
- Streamlit Cloud account (free at https://streamlit.io/cloud)
- API keys (OpenAI or Google)

### Steps

1. **Prepare Repository**
   ```bash
   # Initialize git (if not already)
   git init
   git add .
   git commit -m "Initial commit"
   
   # Create GitHub repository and push
   git remote add origin https://github.com/yourusername/ai-profile.git
   git push -u origin main
   ```

2. **Setup Streamlit Cloud**
   - Go to https://share.streamlit.io/
   - Click "New app"
   - Select your repository
   - Set main file path: `app.py`
   - Click "Deploy"

3. **Add Secrets**
   - In Streamlit Cloud dashboard, go to app settings
   - Click "Secrets"
   - Add your environment variables:
   ```toml
   OPENAI_API_KEY = "sk-..."
   # OR
   GOOGLE_API_KEY = "AIza..."
   
   LLM_PROVIDER = "openai"
   MODEL_NAME = "gpt-4o"
   TEMPERATURE = "0.7"
   ```

4. **Upload Vector Database**
   - After first deployment, the app will fail (no vector DB)
   - Run locally: `python scripts/setup_vectordb.py`
   - The `data/vector_store` directory will be created
   - Commit and push to GitHub:
   ```bash
   git add data/vector_store
   git commit -m "Add vector database"
   git push
   ```

5. **Reboot App**
   - Streamlit Cloud will auto-deploy on push
   - Your app is now live!

### Custom Domain (Optional)
- Go to app settings → "Custom domain"
- Add your domain (requires DNS configuration)

---

## Heroku

**Best for**: More control, custom buildpacks, add-ons

### Prerequisites
- Heroku account
- Heroku CLI installed

### Steps

1. **Create Procfile**
   ```bash
   echo "web: streamlit run app.py --server.port=\$PORT" > Procfile
   ```

2. **Create runtime.txt**
   ```bash
   echo "python-3.11.0" > runtime.txt
   ```

3. **Login and Create App**
   ```bash
   heroku login
   heroku create your-ai-profile
   ```

4. **Set Environment Variables**
   ```bash
   heroku config:set OPENAI_API_KEY=sk-...
   heroku config:set LLM_PROVIDER=openai
   heroku config:set MODEL_NAME=gpt-4o
   ```

5. **Deploy**
   ```bash
   git add .
   git commit -m "Deploy to Heroku"
   git push heroku main
   ```

6. **Setup Vector DB**
   ```bash
   # Run locally, then commit vector store
   python scripts/setup_vectordb.py
   git add data/vector_store
   git commit -m "Add vector database"
   git push heroku main
   ```

7. **Open App**
   ```bash
   heroku open
   ```

---

## AWS EC2

**Best for**: Full control, scalability, enterprise deployment

### Prerequisites
- AWS account
- EC2 instance (t2.medium or larger recommended)
- SSH key pair

### Steps

1. **Launch EC2 Instance**
   - AMI: Ubuntu 22.04 LTS
   - Instance type: t2.medium (minimum)
   - Security group: Allow ports 22 (SSH), 8501 (Streamlit)

2. **Connect to Instance**
   ```bash
   ssh -i your-key.pem ubuntu@your-ec2-ip
   ```

3. **Install Dependencies**
   ```bash
   sudo apt update
   sudo apt install python3-pip python3-venv git -y
   ```

4. **Clone Repository**
   ```bash
   git clone https://github.com/yourusername/ai-profile.git
   cd ai-profile
   ```

5. **Setup Environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

6. **Configure Environment Variables**
   ```bash
   cp .env.example .env
   nano .env  # Edit with your API keys
   ```

7. **Setup Vector Database**
   ```bash
   python scripts/setup_vectordb.py
   ```

8. **Run with Screen (keeps running after disconnect)**
   ```bash
   screen -S streamlit
   streamlit run app.py --server.port=8501 --server.address=0.0.0.0
   # Press Ctrl+A, then D to detach
   ```

9. **Access App**
   - Open browser: `http://your-ec2-ip:8501`

### Production Setup with Systemd

1. **Create Service File**
   ```bash
   sudo nano /etc/systemd/system/streamlit.service
   ```
   
   Add:
   ```ini
   [Unit]
   Description=Streamlit AI Profile
   After=network.target

   [Service]
   Type=simple
   User=ubuntu
   WorkingDirectory=/home/ubuntu/ai-profile
   Environment="PATH=/home/ubuntu/ai-profile/venv/bin"
   ExecStart=/home/ubuntu/ai-profile/venv/bin/streamlit run app.py --server.port=8501 --server.address=0.0.0.0
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```

2. **Enable and Start**
   ```bash
   sudo systemctl enable streamlit
   sudo systemctl start streamlit
   sudo systemctl status streamlit
   ```

### Setup Nginx Reverse Proxy (Optional)

```bash
sudo apt install nginx -y
sudo nano /etc/nginx/sites-available/streamlit
```

Add:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
```

Enable:
```bash
sudo ln -s /etc/nginx/sites-available/streamlit /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

---

## Google Cloud Run

**Best for**: Serverless, auto-scaling, pay-per-use

### Prerequisites
- Google Cloud account
- gcloud CLI installed

### Steps

1. **Create Dockerfile**
   ```dockerfile
   FROM python:3.11-slim

   WORKDIR /app

   COPY requirements.txt .
   RUN pip install --no-cache-dir -r requirements.txt

   COPY . .

   EXPOSE 8501

   CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
   ```

2. **Build and Push**
   ```bash
   gcloud auth login
   gcloud config set project your-project-id
   
   gcloud builds submit --tag gcr.io/your-project-id/ai-profile
   ```

3. **Deploy**
   ```bash
   gcloud run deploy ai-profile \
     --image gcr.io/your-project-id/ai-profile \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated \
     --set-env-vars OPENAI_API_KEY=sk-...,LLM_PROVIDER=openai
   ```

---

## Environment Variables

### Required Variables
```bash
# Choose one provider
OPENAI_API_KEY=sk-...
# OR
GOOGLE_API_KEY=AIza...

LLM_PROVIDER=openai  # or "google"
MODEL_NAME=gpt-4o    # or "gemini-2.0-flash-exp"
```

### Optional Variables
```bash
TEMPERATURE=0.7
MAX_TOKENS=1000
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
APP_TITLE="AI-Powered Digital Profile"
DEVELOPER_NAME="Your Name"
```

---

## Security Best Practices

### 1. API Keys
- Never commit API keys to Git
- Use environment variables or secrets management
- Rotate keys regularly
- Use key restrictions (IP, domain)

### 2. .gitignore
Ensure these are in `.gitignore`:
```
.env
*.pyc
__pycache__/
venv/
.DS_Store
```

### 3. Vector Database
- Commit to private repositories only
- Consider encrypting sensitive data
- Regenerate if profile data changes

### 4. Rate Limiting
- Monitor API usage
- Implement caching for common queries
- Set up usage alerts

### 5. HTTPS
- Use SSL/TLS in production
- Configure reverse proxy (Nginx)
- Use Let's Encrypt for free certificates

---

## Monitoring & Maintenance

### Streamlit Cloud
- Built-in analytics
- View logs in dashboard
- Auto-updates on git push

### Self-Hosted
```bash
# View logs
sudo journalctl -u streamlit -f

# Restart service
sudo systemctl restart streamlit

# Check status
sudo systemctl status streamlit
```

### Cost Optimization
- Use smaller models for development (gpt-3.5-turbo)
- Cache common queries
- Monitor API usage dashboards
- Set up billing alerts

---

## Troubleshooting

### App Won't Start
1. Check logs for errors
2. Verify API keys are set
3. Ensure vector database exists
4. Check Python version compatibility

### Chatbot Not Responding
1. Test API keys: `curl https://api.openai.com/v1/models -H "Authorization: Bearer $OPENAI_API_KEY"`
2. Verify vector store: `ls -la data/vector_store/`
3. Check network/firewall settings

### High Latency
1. Use faster model (gpt-4o-mini, gemini-flash)
2. Reduce chunk size
3. Implement caching
4. Use CDN for static assets

---

## Support & Updates

For issues or questions:
1. Check GitHub issues
2. Review Streamlit documentation
3. Contact: your.email@example.com

---

**Deployment Checklist:**
- [ ] Code pushed to GitHub
- [ ] API keys configured
- [ ] Vector database created
- [ ] Environment variables set
- [ ] Profile photo added
- [ ] Deployment platform chosen
- [ ] App deployed and tested
- [ ] Custom domain configured (optional)
- [ ] Monitoring setup
- [ ] Security review completed

**Estimated Time:**
- Streamlit Cloud: 15-30 minutes
- Heroku: 30-45 minutes
- AWS EC2: 1-2 hours
- Google Cloud Run: 45-60 minutes