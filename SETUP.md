# HODL Platform - Local Development Setup Guide

This guide provides step-by-step instructions to set up and run the HODL decentralized platform locally.

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Environment Setup](#environment-setup)
3. [Installation](#installation)
4. [Database Setup](#database-setup)
5. [Running the Application](#running-the-application)
6. [Testing](#testing)
7. [Configuration](#configuration)

## Prerequisites

### System Requirements
- **Python Version:** 3.11+ (tested with Python 3.12)
- **Operating System:** Linux (Ubuntu/Debian recommended), macOS, or Windows with WSL
- **Required System Packages:**
  - `sqlite3`
  - `git`
  - `python3-dev`
  - `python3-pip`

### Install System Dependencies

**On Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install -y python3 python3-dev python3-pip sqlite3 git
```

**On macOS:**
```bash
brew install python sqlite3
```

**On Windows:**
- Install Python 3.11+ from [python.org](https://www.python.org/downloads/)
- Install SQLite from [sqlite.org](https://www.sqlite.org/download.html)
- Use WSL (Windows Subsystem for Linux) for best compatibility

## Environment Setup

### 1. Clone the Repository
```bash
git clone https://github.com/atharv404/hodl.git
cd hodl
```

### 2. Create Virtual Environment
It's strongly recommended to use a virtual environment to avoid dependency conflicts.

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On Linux/macOS:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

Your terminal prompt should now show `(venv)` prefix.

## Installation

### 1. Install Python Dependencies

Install all required Python packages from requirements.txt:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Note:** The `v8-cffi` package is used for JavaScript smart contract execution. If installation fails, you may need to install libv8 development libraries:

```bash
# On Ubuntu/Debian:
sudo apt install -y libv8-dev

# On macOS:
brew install v8
```

### 2. Install HODL Package

Install the HODL package in development mode:

```bash
python setup.py develop
```

Or for production:
```bash
python setup.py install
```

## Database Setup

The HODL platform uses SQLite for blockchain storage.

### 1. Create Database Directory

```bash
mkdir -p db
```

### 2. Initialize Database

The database will be automatically created when you first run the application. The default database file is `db/bch.db`.

### 3. (Optional) Load Genesis Block

If you need to initialize with a genesis block:

```bash
python -c "from hodl.block.Blockchain import Blockchain; bch = Blockchain(); print('Database initialized')"
```

## Configuration

### Environment Variables

Create a `.env` file in the project root (use `.env.example` as template):

```bash
# Server Configuration
FLASK_HOST=0.0.0.0
FLASK_PORT=8001
FLASK_DEBUG=True

# Database Configuration
DATABASE_PATH=db/bch.db

# Blockchain Configuration
# For testnet/demo purposes, you can use default settings
NETWORK=testnet

# Logging
LOG_LEVEL=INFO
```

### Wallet Configuration

To create a new wallet for testing:

```python
from hodl.wallet.wallet import Wallet
from hodl import cryptogr as cg

# Generate new keys
keys = cg.gen_keys()
print(f"Private Key: {keys[0]}")
print(f"Public Key: {keys[1]}")

# Or create a wallet instance
wallet = Wallet()
print(f"Wallet Public Key: {wallet.pubkey}")
```

Save your keys securely for later use.

## Running the Application

### 1. Start the HODL Daemon

The main entry point is the daemon which runs a Flask REST API server:

```bash
python -m hodl.daemon
```

Or using the module directly:
```bash
cd hodl
python daemon/__init__.py
```

The server will start on `http://localhost:8001` by default.

### 2. Verify the Server

Open another terminal and test the status endpoint:

```bash
curl http://localhost:8001/status
```

Expected response:
```
HDN is available. Version of daemon: 0.1
```

### 3. Available API Endpoints

- `GET /status` - Check daemon status
- `GET /get_block/<int:block_index>` - Get block by index
- `GET /get_sc/<string:sc_index>` - Get smart contract by index
- `GET /get_tnx/<string:tnx_index>` - Get transaction by index

Example:
```bash
# Get the genesis block (block 0)
curl http://localhost:8001/get_block/0
```

## Testing

### Run Unit Tests

```bash
# Run all tests
python -m pytest tests/

# Run specific test modules
python -m pytest tests/block/test_block.py
python -m pytest tests/functional/func_test.py
```

### Run Functional Tests

```bash
cd tests/functional
python func_test.py
```

### Test Wallet Operations

```bash
cd tests/functional
python func_wallet_test.py
```

## Development Mode

For active development with auto-reload:

```bash
# Set Flask environment variables
export FLASK_APP=hodl.daemon
export FLASK_ENV=development
export FLASK_DEBUG=1

# Run with Flask CLI
flask run --host=0.0.0.0 --port=8001
```

## Common Operations

### Create a Transaction

```python
from hodl.wallet.wallet import Wallet
from hodl.block.Blockchain import Blockchain

# Create wallets
sender = Wallet()
receiver_pubkey = "recipient_public_key_here"

# Create transaction
# Syntax: new_transaction(outs, outns, nick)
# where outs is list of recipient addresses and outns is list of amounts
sender.new_transaction([receiver_pubkey], [1.0])
```

### Mine a Block

```python
from hodl.block import mining
from hodl.block.Blockchain import Blockchain

bch = Blockchain()
wallet = Wallet()

# Mine a new block
block = mining.mine(bch)
bch.append(block)
```

### Check Balance

```python
from hodl.block.Blockchain import Blockchain

bch = Blockchain()
pubkey = "your_public_key_here"
balance = bch.money(pubkey)
print(f"Balance: {balance} HDL")
```

## Directory Structure

```
hodl/
├── hodl/                   # Main package
│   ├── block/             # Blockchain implementation
│   ├── cryptogr/          # Cryptography utilities
│   ├── daemon/            # REST API daemon
│   ├── wallet/            # Wallet implementation
│   ├── sc_api/            # Smart contract API
│   └── sync/              # Network synchronization
├── tests/                 # Test suite
├── db/                    # Database directory (created on first run)
├── docs/                  # Documentation
├── requirements.txt       # Python dependencies
└── setup.py              # Package setup
```

## Troubleshooting

See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for common issues and solutions.

## Next Steps

- Read [DEPLOYMENT.md](DEPLOYMENT.md) for production deployment guide
- Explore the smart contract system in `hodl/block/sc/`
- Check out example smart contracts in `tests/scex.py`
- Review the blockchain implementation in `hodl/block/Blockchain.py`

## Support

For issues and questions:
- GitHub Issues: https://github.com/atharv404/hodl/issues
- Original Repository: https://github.com/hodleum/hodl
