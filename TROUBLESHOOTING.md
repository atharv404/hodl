# HODL Platform - Troubleshooting Guide

This guide covers common issues and their solutions when setting up and running the HODL platform.

## Table of Contents
1. [Installation Issues](#installation-issues)
2. [Runtime Errors](#runtime-errors)
3. [Database Issues](#database-issues)
4. [Deployment Problems](#deployment-problems)
5. [Performance Issues](#performance-issues)

## Installation Issues

### Issue: `v8-cffi` Installation Fails

**Error:**
```
error: command 'gcc' failed with exit status 1
fatal error: libplatform/libplatform.h: No such file or directory
```

**Solution 1 - Install libv8 development libraries:**

**On Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install -y libv8-dev build-essential python3-dev
pip install v8-cffi
```

**On macOS:**
```bash
brew install v8
pip install v8-cffi
```

**Solution 2 - Use pre-built wheels:**
```bash
pip install --only-binary :all: v8-cffi
```

**Solution 3 - Skip v8-cffi if not using JS smart contracts:**

If you don't need JavaScript smart contract execution, you can comment out v8-cffi from requirements.txt:
```bash
# Edit requirements.txt and add # before v8-cffi
# v8-cffi
```

### Issue: `flask-restplus` Not Found

**Error:**
```
ModuleNotFoundError: No module named 'flask_restplus'
```

**Solution:**

`flask-restplus` is deprecated. The codebase imports it but doesn't actively use it. Update `hodl/daemon/daemon.py`:

```python
# Remove or comment out:
# from flask_restplus import *

# The Api instance is also not used, so it can be removed
```

Or install the maintained fork:
```bash
pip install flask-restx
```

Then update imports:
```python
from flask_restx import Api
```

### Issue: Permission Denied When Installing Packages

**Error:**
```
PermissionError: [Errno 13] Permission denied
```

**Solution 1 - Use virtual environment (recommended):**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

**Solution 2 - Install with --user flag:**
```bash
pip install --user -r requirements.txt
```

### Issue: Python Version Incompatibility

**Error:**
```
SyntaxError: invalid syntax
```

**Solution:**

Ensure you're using Python 3.11 or higher:
```bash
python3 --version
```

If your system has multiple Python versions:
```bash
# Use specific version
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Issue: SQLAlchemy Version Conflicts

**Error:**
```
ImportError: cannot import name 'declarative_base' from 'sqlalchemy.ext.declarative'
```

**Solution:**

This is due to SQLAlchemy 2.0 changes. The codebase needs updating. For now, use SQLAlchemy 1.4:
```bash
pip install 'sqlalchemy>=1.4,<2.0'
```

## Runtime Errors

### Issue: Database Directory Not Found

**Error:**
```
sqlite3.OperationalError: unable to open database file
FileNotFoundError: [Errno 2] No such file or directory: 'db/bch.db'
```

**Solution:**

Create the database directory:
```bash
mkdir -p db
```

The database file will be created automatically on first run.

### Issue: Import Errors When Running

**Error:**
```
ModuleNotFoundError: No module named 'hodl'
```

**Solution 1 - Install the package:**
```bash
python setup.py develop
# or
python setup.py install
```

**Solution 2 - Add to PYTHONPATH:**
```bash
export PYTHONPATH="${PYTHONPATH}:/path/to/hodl"
python -m hodl.daemon
```

**Solution 3 - Run from correct directory:**
```bash
cd /path/to/hodl
python -m hodl.daemon
```

### Issue: Port Already in Use

**Error:**
```
OSError: [Errno 98] Address already in use
```

**Solution 1 - Kill process using port:**
```bash
# Find process using port 8001
lsof -ti:8001 | xargs kill -9

# Or on Linux:
sudo fuser -k 8001/tcp
```

**Solution 2 - Use different port:**
```python
# Edit hodl/daemon/__init__.py
app.run(host='0.0.0.0', port=8002)  # Change port
```

### Issue: Cryptography Key Generation Errors

**Error:**
```
ValueError: Invalid key format
TypeError: Object of type bytes is not JSON serializable
```

**Solution:**

Ensure keys are properly encoded:
```python
from hodl import cryptogr as cg

# Generate keys
keys = cg.gen_keys()
privkey, pubkey = keys

# Keys might be bytes, convert to string if needed
if isinstance(pubkey, bytes):
    pubkey = pubkey.hex()
if isinstance(privkey, bytes):
    privkey = privkey.hex()
```

### Issue: Flask Debug Mode Reloader Errors

**Error:**
```
SystemExit: 1
Restarting with stat
```

**Solution:**

Disable reloader if causing issues:
```python
app.run(host='0.0.0.0', port=8001, debug=True, use_reloader=False)
```

## Database Issues

### Issue: Database Locked

**Error:**
```
sqlite3.OperationalError: database is locked
```

**Solution 1 - Ensure single connection:**

SQLite doesn't handle concurrent writes well. Ensure only one process writes to the database:
```python
# Use check_same_thread=False carefully
conn = sqlite3.connect('db/bch.db', check_same_thread=False, timeout=30)
```

**Solution 2 - Use WAL mode:**
```python
conn.execute('PRAGMA journal_mode=WAL')
```

**Solution 3 - Close existing connections:**
```bash
# Stop all HODL processes
pkill -f "python.*hodl.daemon"
```

### Issue: Database Corruption

**Error:**
```
sqlite3.DatabaseError: database disk image is malformed
```

**Solution 1 - Restore from backup:**
```bash
cp db/bch.db.backup db/bch.db
```

**Solution 2 - Try to recover:**
```bash
sqlite3 db/bch.db "PRAGMA integrity_check"
sqlite3 db/bch.db ".dump" | sqlite3 db/bch_recovered.db
mv db/bch_recovered.db db/bch.db
```

**Solution 3 - Start fresh (development only):**
```bash
rm db/bch.db
# Database will be recreated
```

### Issue: Migration Errors

**Error:**
```
Table 'blocks' already exists
```

**Solution:**

Check if database needs initialization:
```python
from hodl.block.Blockchain import Blockchain

bch = Blockchain()
# If table exists, it will use it
# If not, it will create it
```

## Deployment Problems

### Issue: Vercel Deployment - Module Not Found

**Error:**
```
ModuleNotFoundError: No module named 'hodl'
```

**Solution:**

Ensure proper directory structure:
```
project/
├── api/
│   ├── index.py
│   └── requirements.txt
├── hodl/
│   └── (package files)
└── vercel.json
```

Update `vercel.json` to include Python files:
```json
{
  "builds": [
    {
      "src": "api/index.py",
      "use": "@vercel/python",
      "config": {
        "includeFiles": ["hodl/**"]
      }
    }
  ]
}
```

### Issue: Vercel - Function Size Too Large

**Error:**
```
Error: Serverless Function size exceeds 50 MB limit
```

**Solution:**

Reduce dependencies in `api/requirements.txt`:
```
flask==3.1.2
sqlalchemy==2.0.44
werkzeug==3.1.3
# Only include essential packages
```

Remove unnecessary dependencies like docker, fabric, vagrant.

### Issue: Railway/Render - Build Timeout

**Error:**
```
Build timed out after 15 minutes
```

**Solution:**

Optimize installation:
```bash
# In Procfile or start command
pip install --no-cache-dir -r requirements.txt
```

### Issue: Docker Container Won't Start

**Error:**
```
Container exited with code 1
```

**Solution:**

Check logs:
```bash
docker logs <container_id>
```

Common fixes:
```dockerfile
# Ensure working directory exists
RUN mkdir -p /app/db /app/logs

# Set proper permissions
RUN chmod -R 755 /app

# Use proper Python path
CMD ["python", "-m", "hodl.daemon"]
```

### Issue: CORS Errors in Production

**Error (in browser console):**
```
Access to fetch at 'https://api.hodl.com' from origin 'https://app.hodl.com' 
has been blocked by CORS policy
```

**Solution:**

Add CORS support:
```python
from flask_cors import CORS

# Allow all origins (development only)
CORS(app)

# Or specific origins (production)
CORS(app, resources={
    r"/api/*": {
        "origins": ["https://app.hodl.com"],
        "methods": ["GET", "POST"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})
```

Install flask-cors:
```bash
pip install flask-cors
```

## Performance Issues

### Issue: Slow API Response Times

**Symptoms:**
- API requests take > 5 seconds
- Timeout errors

**Solution 1 - Add database indexes:**
```sql
CREATE INDEX idx_blocks_hash ON blocks(hash);
CREATE INDEX idx_transactions_from ON transactions(from_address);
```

**Solution 2 - Implement caching:**
```python
from flask_caching import Cache

cache = Cache(app, config={'CACHE_TYPE': 'simple'})

@app.route('/api/block/<int:index>')
@cache.cached(timeout=300)
def get_block(index):
    # Cached for 5 minutes
    pass
```

**Solution 3 - Optimize queries:**
```python
# Instead of loading full blockchain
# Only query needed data
block = bch.get_block_by_index(index)
```

### Issue: High Memory Usage

**Symptoms:**
- Application crashes with memory errors
- OOM (Out of Memory) kills

**Solution 1 - Limit blockchain in memory:**
```python
# Don't load entire blockchain
# Query database directly for specific blocks
```

**Solution 2 - Increase swap space (Linux):**
```bash
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

**Solution 3 - Optimize smart contract execution:**
```python
# Set memory limits for smart contracts
# Limit execution time
```

### Issue: Mining Takes Too Long

**Symptoms:**
- Mining never completes
- CPU at 100% for extended periods

**Solution:**

Adjust mining difficulty for testnet:
```python
# Use lower difficulty for demo/testing
difficulty = 1000000  # Instead of very high difficulty
n, t, h = mining.pow_mine(bch, difficulty, pubkey)
```

## Development Issues

### Issue: Tests Failing

**Error:**
```
ImportError in test files
AssertionError in test cases
```

**Solution:**

Run tests from correct location:
```bash
# From project root
python -m pytest tests/

# Or specific test
python -m pytest tests/block/test_block.py -v
```

Ensure test dependencies are installed:
```bash
pip install pytest pytest-cov
```

### Issue: IDE Import Warnings

**Symptoms:**
- Red underlines in IDE
- "Cannot find reference" warnings

**Solution:**

Mark directories as source roots in your IDE:
- PyCharm: Right-click `hodl` folder → Mark Directory as → Sources Root
- VS Code: Add to `settings.json`:
  ```json
  {
    "python.analysis.extraPaths": [
      "./hodl"
    ]
  }
  ```

## Getting Help

If your issue isn't covered here:

1. **Check logs:**
   ```bash
   # Application logs
   tail -f logs/hodl.log
   
   # System logs
   journalctl -u hodl -f
   ```

2. **Enable debug mode:**
   ```python
   app.run(debug=True)
   ```

3. **Search existing issues:**
   - https://github.com/atharv404/hodl/issues
   - https://github.com/hodleum/hodl/issues

4. **Create a new issue:**
   - Include error messages
   - Provide system information
   - Share relevant logs
   - Describe steps to reproduce

5. **Community Support:**
   - GitHub Discussions
   - Stack Overflow (tag: hodl-blockchain)

## Common Error Messages Quick Reference

| Error Message | Likely Cause | Quick Fix |
|--------------|--------------|-----------|
| `ModuleNotFoundError: No module named 'hodl'` | Package not installed | Run `python setup.py develop` |
| `sqlite3.OperationalError: unable to open database` | Missing db directory | Run `mkdir -p db` |
| `OSError: [Errno 98] Address already in use` | Port conflict | Kill process or change port |
| `ImportError: cannot import name 'declarative_base'` | SQLAlchemy version | Install SQLAlchemy 1.4.x |
| `fatal error: libplatform/libplatform.h` | Missing v8 libraries | Install libv8-dev |
| `database is locked` | Concurrent access | Ensure single writer |
| `Serverless Function size exceeds limit` | Too many dependencies | Minimize requirements.txt |
| `CORS policy blocked` | CORS not configured | Add flask-cors |

## Preventive Measures

1. **Always use virtual environment**
2. **Keep backups of database**
3. **Monitor logs regularly**
4. **Test in staging before production**
5. **Use version control (Git)**
6. **Document configuration changes**
7. **Set up monitoring and alerts**
8. **Regular security updates**

## Additional Resources

- [SETUP.md](SETUP.md) - Setup guide
- [DEPLOYMENT.md](DEPLOYMENT.md) - Deployment guide
- [README.md](README.md) - Project overview
- Original documentation: https://github.com/hodleum/hodl
