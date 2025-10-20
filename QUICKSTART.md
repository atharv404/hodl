# HODL Platform - Quick Start Guide

Get up and running with HODL in 5 minutes!

## Prerequisites

- Python 3.11 or higher
- Git

## Installation (Linux/macOS)

```bash
# 1. Clone the repository
git clone https://github.com/atharv404/hodl.git
cd hodl

# 2. Run the automated setup script
chmod +x scripts/setup.sh
./scripts/setup.sh

# 3. Start the daemon
source venv/bin/activate  # Activate virtual environment
python -m hodl.daemon
```

The daemon will start on http://localhost:8001

## Installation (Windows)

```powershell
# 1. Clone the repository
git clone https://github.com/atharv404/hodl.git
cd hodl

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt
python setup.py develop

# 4. Create database directory
mkdir db

# 5. Start the daemon
python -m hodl.daemon
```

## Manual Installation (All Platforms)

```bash
# 1. Clone and navigate
git clone https://github.com/atharv404/hodl.git
cd hodl

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# 4. Install HODL package
python setup.py develop

# 5. Create necessary directories
mkdir -p db logs

# 6. Create .env file (optional)
cp .env.example .env

# 7. Start the daemon
python -m hodl.daemon
```

## Verify Installation

Open another terminal and test:

```bash
# Check status
curl http://localhost:8001/status

# Expected response:
# HDN is available. Version of daemon: 0.1
```

## Quick Test

```bash
# Get genesis block (block 0)
curl http://localhost:8001/get_block/0
```

## Create Your First Wallet

```python
# Open Python REPL
python

# Create a wallet
from hodl.wallet.wallet import Wallet
wallet = Wallet()
print(f"Your public key: {wallet.pubkey}")
```

## Deploy to Vercel (Demo API)

```bash
# 1. Install Vercel CLI
npm i -g vercel

# 2. Login to Vercel
vercel login

# 3. Deploy
vercel --prod
```

Your demo API will be live at: `https://your-project.vercel.app`

## Deploy with Docker

```bash
# Build and run
docker-compose up -d

# Check logs
docker-compose logs -f

# Stop
docker-compose down
```

## Deploy to Railway

```bash
# 1. Install Railway CLI
npm i -g @railway/cli

# 2. Login and deploy
railway login
railway init
railway up
```

## Next Steps

### For Development
- Read [SETUP.md](SETUP.md) for detailed setup instructions
- Explore smart contracts in `hodl/block/sc/`
- Check examples in `tests/`

### For Deployment
- Read [DEPLOYMENT.md](DEPLOYMENT.md) for production deployment
- Configure environment variables from `.env.example`
- Set up monitoring and backups

### For Troubleshooting
- Read [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
- Check GitHub issues
- Enable debug mode: `export FLASK_DEBUG=1`

## API Endpoints

Once running, these endpoints are available:

| Endpoint | Description | Example |
|----------|-------------|---------|
| `GET /status` | Check daemon status | `curl http://localhost:8001/status` |
| `GET /get_block/<index>` | Get block by index | `curl http://localhost:8001/get_block/0` |
| `GET /get_sc/<sc_index>` | Get smart contract | `curl http://localhost:8001/get_sc/[0,0]` |
| `GET /get_tnx/<tnx_index>` | Get transaction | `curl http://localhost:8001/get_tnx/[0,0]` |

## Common Issues

### Port Already in Use
```bash
# Kill process on port 8001
lsof -ti:8001 | xargs kill -9
```

### Import Errors
```bash
# Reinstall package
python setup.py develop
```

### Database Not Found
```bash
# Create database directory
mkdir -p db
```

### Virtual Environment Not Active
```bash
# Activate it
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

## Features Overview

### ✨ Smart Contracts
Write smart contracts in Python 3:
```python
from hodl.block.Blockchain import Blockchain

bch = Blockchain()
with open('contract.py', 'r') as f:
    bch.new_sc(f.readlines(), wallet.pubkey, wallet.privkey)
```

### 💰 Transactions
Send HODL tokens:
```python
wallet.new_transaction(
    [recipient_pubkey],  # Recipients
    [1.0]                # Amounts
)
```

### ⛏️ Mining
Mine new blocks:
```python
from hodl.block import mining

block = mining.mine(bch)
bch.append(block)
```

### 💼 Check Balance
```python
balance = bch.money(wallet.pubkey)
print(f"Balance: {balance} HDL")
```

## Architecture

```
┌─────────────────────────────────────────┐
│         REST API (Flask)                │
│       localhost:8001                    │
└───────────────┬─────────────────────────┘
                │
┌───────────────▼─────────────────────────┐
│        Blockchain Layer                 │
│   - Block Management                    │
│   - Transaction Processing              │
│   - Smart Contract Execution            │
└───────────────┬─────────────────────────┘
                │
┌───────────────▼─────────────────────────┐
│      Storage Layer (SQLite)             │
│         db/bch.db                       │
└─────────────────────────────────────────┘
```

## Development Workflow

```bash
# 1. Make changes to code
vim hodl/daemon/daemon.py

# 2. Test changes
python -m hodl.daemon

# 3. Run tests (if available)
pytest tests/

# 4. Commit changes
git add .
git commit -m "Your changes"
git push
```

## Production Checklist

- [ ] Set `FLASK_DEBUG=False` in production
- [ ] Use strong `SECRET_KEY` in `.env`
- [ ] Enable HTTPS/SSL
- [ ] Set up database backups
- [ ] Configure monitoring (Sentry, etc.)
- [ ] Set up log rotation
- [ ] Use production WSGI server (gunicorn)
- [ ] Configure firewall rules
- [ ] Set up reverse proxy (nginx)
- [ ] Regular security updates

## Resources

- **Documentation**: See [SETUP.md](SETUP.md), [DEPLOYMENT.md](DEPLOYMENT.md), [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
- **GitHub**: https://github.com/atharv404/hodl
- **Original Project**: https://github.com/hodleum/hodl
- **Issues**: https://github.com/atharv404/hodl/issues

## License

Apache 2.0

---

**Ready to build on HODL?** Start with the examples in the `tests/` directory!
