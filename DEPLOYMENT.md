# HODL Platform - Production Deployment Guide

This guide provides comprehensive instructions for deploying the HODL decentralized platform to production environments, with specific focus on Vercel and serverless platforms.

## Table of Contents
1. [Deployment Considerations](#deployment-considerations)
2. [Vercel Deployment](#vercel-deployment)
3. [Alternative Serverless Platforms](#alternative-serverless-platforms)
4. [Traditional Server Deployment](#traditional-server-deployment)
5. [Security Best Practices](#security-best-practices)
6. [Monitoring and Maintenance](#monitoring-and-maintenance)

## Deployment Considerations

### Platform Limitations

**Important:** The HODL platform has specific characteristics that affect deployment options:

1. **Stateful SQLite Database**: The application uses SQLite which requires persistent file storage
2. **Long-Running Processes**: Mining operations may run for extended periods
3. **WebSocket Support**: May be needed for real-time blockchain synchronization
4. **Computational Requirements**: Smart contract execution and mining require CPU resources

### Recommended Deployment Approach

Given these requirements, **pure serverless platforms like Vercel have limitations** for this application:

- ✅ **Good for:** Demo/read-only blockchain explorer API
- ⚠️ **Limited for:** Full blockchain node with mining and transactions
- ❌ **Not suitable for:** Production blockchain network with persistent state

**Best Options:**
1. **Hybrid Approach**: Vercel for API + External database (PostgreSQL/MongoDB)
2. **Container Platform**: Railway, Render, DigitalOcean App Platform
3. **VPS/Dedicated Server**: For full blockchain node functionality

## Vercel Deployment

### Approach 1: Read-Only API Demo (Recommended for Vercel)

This approach deploys a read-only blockchain explorer API suitable for demos.

#### Step 1: Prepare the Application

Create a serverless-compatible entry point at `api/index.py`:

```python
from flask import Flask, jsonify
from hodl.block.Blockchain import Blockchain
import os

app = Flask(__name__)

# Initialize blockchain in read-only mode
bch = Blockchain(filename='bch.db', m='ro')

@app.route('/')
def home():
    return jsonify({
        'status': 'online',
        'version': '0.1',
        'description': 'HODL Blockchain Explorer API',
        'endpoints': {
            'status': '/api/status',
            'block': '/api/block/<int:index>',
            'stats': '/api/stats'
        }
    })

@app.route('/api/status')
def status():
    return jsonify({
        'status': 'online',
        'version': '0.1',
        'mode': 'read-only',
        'blockchain_length': len(bch) if hasattr(bch, '__len__') else 0
    })

@app.route('/api/block/<int:index>')
def get_block(index):
    try:
        block = str(bch[index])
        return jsonify({'block': block, 'index': index})
    except Exception as e:
        return jsonify({'error': str(e)}), 404

@app.route('/api/stats')
def stats():
    try:
        return jsonify({
            'total_blocks': len(bch) if hasattr(bch, '__len__') else 0,
            'database': 'SQLite',
            'network': 'testnet'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Vercel serverless handler
def handler(request):
    return app(request.environ, request.start_response)
```

#### Step 2: Create vercel.json

```json
{
  "version": 2,
  "name": "hodl-blockchain-explorer",
  "builds": [
    {
      "src": "api/index.py",
      "use": "@vercel/python",
      "config": {
        "maxLambdaSize": "50mb"
      }
    }
  ],
  "routes": [
    {
      "src": "/api/(.*)",
      "dest": "api/index.py"
    },
    {
      "src": "/(.*)",
      "dest": "api/index.py"
    }
  ],
  "env": {
    "PYTHONUNBUFFERED": "1"
  }
}
```

#### Step 3: Update requirements.txt for Vercel

Create `api/requirements.txt`:

```
flask==3.1.2
sqlalchemy==2.0.44
werkzeug==3.1.3
pycryptodome==3.23.0
```

#### Step 4: Deploy to Vercel

```bash
# Install Vercel CLI
npm i -g vercel

# Login to Vercel
vercel login

# Deploy
vercel --prod
```

#### Step 5: Pre-populate Database

Since Vercel's filesystem is read-only, pre-populate a demo database:

```bash
# Create and populate database locally
python scripts/create_demo_db.py

# Include db/ directory in deployment
# Add to .vercelignore (do NOT ignore db/):
```

Create `.vercelignore`:
```
__pycache__/
*.pyc
.git/
tests/
docs/
venv/
.env
```

### Approach 2: External Database (PostgreSQL)

For a more robust solution, migrate from SQLite to PostgreSQL:

#### Step 1: Add PostgreSQL Support

Update `requirements.txt`:
```
flask==3.1.2
sqlalchemy==2.0.44
psycopg2-binary==2.9.9
werkzeug==3.1.3
pycryptodome==3.23.0
```

#### Step 2: Configure Database Connection

Set environment variables in Vercel dashboard:
```
DATABASE_URL=postgresql://user:password@host:5432/hodl
ENVIRONMENT=production
```

#### Step 3: Modify Blockchain Class

Update `hodl/block/Blockchain.py` to support PostgreSQL (or create an adapter).

## Alternative Serverless Platforms

### Railway.app (Recommended)

Railway provides persistent storage and is well-suited for this application.

**Deployment:**

1. Create `railway.json`:
```json
{
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "python -m hodl.daemon",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

2. Create `Procfile`:
```
web: python -m hodl.daemon
```

3. Deploy:
```bash
# Install Railway CLI
npm i -g @railway/cli

# Login and deploy
railway login
railway init
railway up
```

**Benefits:**
- Persistent volumes for SQLite
- Always-on dynos (no cold starts)
- Better for long-running processes

### Render.com

Similar to Railway with persistent disks.

**Deployment:**

1. Create `render.yaml`:
```yaml
services:
  - type: web
    name: hodl-node
    env: python
    buildCommand: pip install -r requirements.txt && python setup.py install
    startCommand: python -m hodl.daemon
    plan: starter
    envVars:
      - key: FLASK_HOST
        value: 0.0.0.0
      - key: FLASK_PORT
        value: 8001
    disk:
      name: hodl-data
      mountPath: /app/db
      sizeGB: 1
```

2. Deploy via Render dashboard or CLI

### Heroku

**Deployment:**

1. Create `Procfile`:
```
web: python -m hodl.daemon
```

2. Create `runtime.txt`:
```
python-3.11.0
```

3. Deploy:
```bash
heroku create hodl-blockchain
heroku addons:create heroku-postgresql:mini
git push heroku main
```

## Traditional Server Deployment

### Docker Deployment (Recommended for Production)

#### Step 1: Update Dockerfile

See the updated `Dockerfile` in the repository.

#### Step 2: Docker Compose

Create `docker-compose.yml`:
```yaml
version: '3.8'

services:
  hodl-node:
    build: .
    ports:
      - "8001:8001"
    volumes:
      - hodl-data:/app/db
      - hodl-logs:/app/logs
    environment:
      - FLASK_HOST=0.0.0.0
      - FLASK_PORT=8001
      - DATABASE_PATH=/app/db/bch.db
      - LOG_LEVEL=INFO
    restart: unless-stopped
    networks:
      - hodl-network

volumes:
  hodl-data:
  hodl-logs:

networks:
  hodl-network:
    driver: bridge
```

#### Step 3: Deploy

```bash
docker-compose up -d
```

### VPS Deployment (DigitalOcean, AWS EC2, etc.)

#### Step 1: Provision Server

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install dependencies
sudo apt install -y python3.11 python3.11-venv python3-pip sqlite3 git nginx certbot python3-certbot-nginx
```

#### Step 2: Setup Application

```bash
# Clone repository
cd /opt
sudo git clone https://github.com/atharv404/hodl.git
cd hodl

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
python setup.py install

# Create directories
sudo mkdir -p /opt/hodl/db /opt/hodl/logs
```

#### Step 3: Create Systemd Service

Create `/etc/systemd/system/hodl.service`:

```ini
[Unit]
Description=HODL Blockchain Node
After=network.target

[Service]
Type=simple
User=hodl
Group=hodl
WorkingDirectory=/opt/hodl
Environment="PATH=/opt/hodl/venv/bin"
ExecStart=/opt/hodl/venv/bin/python -m hodl.daemon
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl daemon-reload
sudo systemctl enable hodl
sudo systemctl start hodl
sudo systemctl status hodl
```

#### Step 4: Setup Nginx Reverse Proxy

Create `/etc/nginx/sites-available/hodl`:

```nginx
server {
    listen 80;
    server_name hodl.yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:8001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # WebSocket support
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

Enable site:
```bash
sudo ln -s /etc/nginx/sites-available/hodl /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

#### Step 5: Setup SSL with Let's Encrypt

```bash
sudo certbot --nginx -d hodl.yourdomain.com
```

## Security Best Practices

### 1. Environment Variables

**Never commit secrets to Git.** Use environment variables for sensitive data:

```bash
# .env file (add to .gitignore)
SECRET_KEY=your-secret-key-here
DATABASE_URL=postgresql://...
API_KEY=your-api-key

# Load in application
from dotenv import load_dotenv
load_dotenv()
```

### 2. API Rate Limiting

Implement rate limiting to prevent abuse:

```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["100 per minute"]
)

@app.route('/api/block/<int:index>')
@limiter.limit("10 per minute")
def get_block(index):
    # ...
```

### 3. CORS Configuration

Configure CORS properly for production:

```python
from flask_cors import CORS

CORS(app, resources={
    r"/api/*": {
        "origins": ["https://yourdomain.com"],
        "methods": ["GET", "POST"],
        "allow_headers": ["Content-Type"]
    }
})
```

### 4. Database Security

- Use encrypted connections for remote databases
- Regular backups
- Implement proper access controls
- Monitor for unusual activity

### 5. HTTPS/SSL

Always use HTTPS in production:
- Let's Encrypt for free SSL certificates
- Configure strict HTTPS redirect
- Enable HSTS headers

## Monitoring and Maintenance

### Logging

Configure comprehensive logging:

```python
import logging
import logging.handlers

# Setup rotating file handler
handler = logging.handlers.RotatingFileHandler(
    'logs/hodl.log',
    maxBytes=10485760,  # 10MB
    backupCount=5
)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    handlers=[handler, logging.StreamHandler()]
)
```

### Health Check Endpoint

```python
@app.route('/health')
def health():
    return jsonify({
        'status': 'healthy',
        'timestamp': time.time(),
        'uptime': time.time() - start_time
    })
```

### Monitoring Services

- **Uptime Monitoring**: UptimeRobot, Pingdom
- **Application Monitoring**: New Relic, Datadog
- **Log Aggregation**: Loggly, Papertrail
- **Error Tracking**: Sentry, Rollbar

### Backup Strategy

```bash
# Backup script (backup.sh)
#!/bin/bash
BACKUP_DIR="/backups/hodl"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# Backup database
cp /opt/hodl/db/bch.db "$BACKUP_DIR/bch_$TIMESTAMP.db"

# Compress
gzip "$BACKUP_DIR/bch_$TIMESTAMP.db"

# Remove backups older than 30 days
find "$BACKUP_DIR" -name "*.gz" -mtime +30 -delete
```

Automate with cron:
```bash
# Run backup daily at 2 AM
0 2 * * * /opt/hodl/scripts/backup.sh
```

## Performance Optimization

### 1. Caching

Implement caching for frequently accessed data:

```python
from flask_caching import Cache

cache = Cache(app, config={
    'CACHE_TYPE': 'simple',
    'CACHE_DEFAULT_TIMEOUT': 300
})

@app.route('/api/stats')
@cache.cached(timeout=60)
def stats():
    # Expensive operation
    return jsonify(calculate_stats())
```

### 2. Database Optimization

- Use indexes for frequently queried fields
- Implement connection pooling
- Consider read replicas for scaling

### 3. Load Balancing

For high-traffic deployments, use load balancer:
- Nginx load balancing
- AWS ELB/ALB
- Cloudflare Load Balancing

## Cost Estimation

### Vercel (Read-Only Demo)
- **Free Tier**: Limited requests, good for demos
- **Pro**: $20/month for 100GB bandwidth

### Railway
- **Free Tier**: $5 credit/month (enough for small demo)
- **Paid**: ~$10-30/month depending on usage

### VPS (Full Node)
- **DigitalOcean Droplet**: $6-12/month (basic)
- **AWS EC2**: Variable, ~$10-30/month
- **Domain**: $10-15/year
- **SSL**: Free (Let's Encrypt)

## Troubleshooting Production Issues

See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for common deployment issues and solutions.

## Next Steps

1. Choose deployment platform based on requirements
2. Set up monitoring and alerting
3. Implement backup strategy
4. Configure CI/CD pipeline
5. Load testing and optimization
6. Documentation for API consumers

## Support

For deployment assistance:
- GitHub Issues: https://github.com/atharv404/hodl/issues
- Community: Create discussions for deployment questions
