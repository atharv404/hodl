# HODL
**HODL is a decentralized platform for payments, computing, storing and DApps.**

It has smart contracts which can be written in Python 3. **HODL** uses Proofs-of-work and Proofs-of-stake together. It is also a platform for decentralized internet.
**HODL** will have clients for Linux, Windows, OS X, Android and IOS. It will support NFC.

[![Build Status](https://travis-ci.org/hodleum/hodl.svg?branch=master)](https://travis-ci.org/hodleum/hodl)
[![Python Version](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-Apache%202.0-green.svg)](LICENSE)

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/atharv404/hodl.git
cd hodl

# Run automated setup (Linux/macOS)
chmod +x scripts/setup.sh
./scripts/setup.sh

# Start the daemon
source venv/bin/activate
python -m hodl.daemon
```

Visit http://localhost:8001/status to verify it's running!

**For detailed instructions**, see [QUICKSTART.md](QUICKSTART.md)

## 📖 Documentation

- **[Quick Start Guide](QUICKSTART.md)** - Get running in 5 minutes
- **[Setup Guide](SETUP.md)** - Detailed local development setup
- **[Deployment Guide](DEPLOYMENT.md)** - Deploy to production (Vercel, Railway, Docker, VPS)
- **[Troubleshooting](TROUBLESHOOTING.md)** - Common issues and solutions

## Installation Options

### Option 1: Automated Setup (Recommended)
**On Linux/macOS:**
```bash
git clone https://github.com/atharv404/hodl.git
cd hodl
chmod +x scripts/setup.sh
./scripts/setup.sh
```

### Option 2: Manual Setup
**On any platform:**
```bash
git clone https://github.com/atharv404/hodl.git
cd hodl
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python setup.py develop
mkdir -p db logs
python -m hodl.daemon
```

### Option 3: Docker
```bash
git clone https://github.com/atharv404/hodl.git
cd hodl
docker-compose up -d
```

## 🌐 Deploy to Production

### Deploy to Vercel (Serverless Demo)
```bash
npm i -g vercel
vercel --prod
```

### Deploy to Railway (Full Node)
```bash
npm i -g @railway/cli
railway init
railway up
```

### Deploy with Docker
```bash
docker-compose up -d
```

See [DEPLOYMENT.md](DEPLOYMENT.md) for complete deployment guides including Heroku, Render, and VPS options.

## ✨ Features

### 🔗 Smart Contracts
* **Easy to Write** - Smart contracts are written in Python 3, one of the most popular and easiest programming languages
* **Powerful** - Use any Python library, create multi-file contracts, and build complex decentralized applications
* **Flexible** - Support for graphical and web interfaces

### 💻 Decentralized Computing
Purchase verifiable computing power at low costs. Miners receive new tokens as part of the block reward, keeping prices competitive.

### 💾 Decentralized Storage
Store encrypted data on the HODL network at affordable prices, enabled by the token reward system.

### 🌍 Decentralized Internet (HDI)
Smart contracts can have graphical interfaces written in HML (HODL Markup Language) and custom domain names, creating a truly decentralized internet.

### ⛏️ Hybrid Consensus
Combines Proof-of-Work (PoW) and Proof-of-Stake (PoS) for security and efficiency.

## 🔧 API Endpoints

Once the daemon is running, these REST API endpoints are available:

| Endpoint | Method | Description | Example |
|----------|--------|-------------|---------|
| `/status` | GET | Check daemon status | `curl http://localhost:8001/status` |
| `/get_block/<index>` | GET | Get block by index | `curl http://localhost:8001/get_block/0` |
| `/get_sc/<sc_index>` | GET | Get smart contract | `curl http://localhost:8001/get_sc/[0,0]` |
| `/get_tnx/<tnx_index>` | GET | Get transaction | `curl http://localhost:8001/get_tnx/[0,0]` |

## 🏗️ Architecture

```
┌─────────────────────────────────────────┐
│         REST API Layer (Flask)          │
│            Port 8001                    │
└───────────────┬─────────────────────────┘
                │
┌───────────────▼─────────────────────────┐
│        Blockchain Layer                 │
│   • Block Management                    │
│   • Transaction Processing              │
│   • Smart Contract Execution            │
│   • Mining (PoW + PoS)                  │
└───────────────┬─────────────────────────┘
                │
┌───────────────▼─────────────────────────┐
│    Storage Layer (SQLite/PostgreSQL)    │
│           db/bch.db                     │
└─────────────────────────────────────────┘
```

## 🛠️ Technology Stack

- **Language**: Python 3.11+
- **Web Framework**: Flask
- **Database**: SQLite (default) / PostgreSQL (production)
- **Cryptography**: pycryptodome
- **Smart Contracts**: Python 3 (with optional JavaScript via v8-cffi)
- **Network**: Twisted

## 📦 Requirements

- **Python**: 3.11 or higher (tested with 3.12)
- **Operating System**: Linux, macOS, Windows (WSL recommended)
- **Database**: SQLite3 (included) or PostgreSQL (optional)
- **Memory**: 512MB+ RAM recommended
- **Disk**: 1GB+ for blockchain data

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

Apache 2.0

## 🔗 Links

- **Repository**: https://github.com/atharv404/hodl
- **Original Project**: https://github.com/hodleum/hodl
- **Issues**: https://github.com/atharv404/hodl/issues

## 🙏 Credits

Original HODL project by [hodleum](https://github.com/hodleum)

---

**Built with 💙 for the decentralized future**
