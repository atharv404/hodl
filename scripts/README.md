# HODL Platform - Scripts

This directory contains utility scripts for setting up and managing the HODL platform.

## Available Scripts

### 1. setup.sh
**Automated installation script for local development**

**Purpose**: Automates the entire setup process including virtual environment creation, dependency installation, and database initialization.

**Usage**:
```bash
chmod +x scripts/setup.sh
./scripts/setup.sh
```

**What it does**:
- Checks Python version (requires 3.11+)
- Creates and activates virtual environment
- Installs system dependencies (on Linux)
- Installs Python dependencies
- Installs HODL package in development mode
- Creates necessary directories (db/, logs/, tmp/)
- Creates .env file from template
- Initializes database
- Runs basic tests

**Time**: ~5 minutes

**Requirements**:
- Python 3.11 or higher
- Internet connection for package downloads
- sudo access (for system dependencies)

---

### 2. create_demo_db.py
**Demo database creation script**

**Purpose**: Creates a pre-populated database with sample wallets and blockchain data for demonstration and testing purposes.

**Usage**:
```bash
# Make executable
chmod +x scripts/create_demo_db.py

# Run the script
python scripts/create_demo_db.py

# Or directly
./scripts/create_demo_db.py
```

**What it does**:
- Initializes a fresh blockchain database
- Creates 3 demo wallets (Alice, Bob, Charlie)
- Generates key pairs for each wallet
- Saves wallet information to `demo_wallets.json`
- Sets up genesis block

**Output**:
- Database file: `db/bch.db`
- Wallet info: `demo_wallets.json`

**Time**: ~30 seconds

**Requirements**:
- Python 3.11 or higher
- HODL package installed

---

## Script Details

### setup.sh

**Features**:
- ✅ Colored output for better UX
- ✅ Error handling and validation
- ✅ Cross-platform support (Linux/macOS)
- ✅ Idempotent (safe to run multiple times)
- ✅ User confirmation for system changes

**Exit Codes**:
- `0` - Success
- `1` - Error occurred

**Environment Variables** (optional):
- `PYTHON` - Python executable to use (default: python3)
- `VENV_DIR` - Virtual environment directory (default: venv)

**Example with custom settings**:
```bash
PYTHON=python3.11 VENV_DIR=myenv ./scripts/setup.sh
```

---

### create_demo_db.py

**Features**:
- ✅ Clean database creation
- ✅ Sample wallet generation
- ✅ JSON output for wallet info
- ✅ Error handling
- ✅ Progress reporting

**Output Format** (demo_wallets.json):
```json
{
  "Alice": {
    "public_key": "abc123...",
    "description": "First demo user"
  },
  "Bob": {
    "public_key": "def456...",
    "description": "Second demo user"
  },
  "Charlie": {
    "public_key": "ghi789...",
    "description": "Third demo user"
  }
}
```

**Use Cases**:
- Quick testing
- Demo presentations
- Development
- Tutorial walkthroughs

---

## Adding New Scripts

When adding new scripts to this directory:

1. **Follow naming convention**: Use lowercase with underscores (e.g., `backup_db.sh`)
2. **Add shebang**: Start with `#!/usr/bin/env bash` or `#!/usr/bin/env python3`
3. **Make executable**: `chmod +x scripts/your_script.sh`
4. **Add to this README**: Document what it does
5. **Add help text**: Include `-h` or `--help` option
6. **Error handling**: Exit with appropriate codes
7. **User-friendly**: Add progress output

**Template for new bash scripts**:
```bash
#!/usr/bin/env bash
set -e  # Exit on error

# Script name and description
echo "Script Name - Short description"
echo ""

# Check requirements
if ! command -v required_tool &> /dev/null; then
    echo "Error: required_tool not found"
    exit 1
fi

# Main logic
echo "Doing something..."
# ... your code ...

echo "Done!"
```

**Template for new Python scripts**:
```python
#!/usr/bin/env python3
"""
Script Name - Short description

Usage:
    python script_name.py [options]
"""

import sys
import os

def main():
    """Main function"""
    try:
        # Your code here
        print("Doing something...")
        return 0
    except Exception as e:
        print(f"Error: {e}")
        return 1

if __name__ == '__main__':
    sys.exit(main())
```

---

## Troubleshooting

### setup.sh Issues

**Problem**: Permission denied
```bash
# Solution: Make executable
chmod +x scripts/setup.sh
```

**Problem**: Python version too old
```bash
# Solution: Install Python 3.11+
# On Ubuntu:
sudo apt install python3.11
```

**Problem**: Virtual environment activation fails
```bash
# Solution: Source it manually
source venv/bin/activate
```

### create_demo_db.py Issues

**Problem**: Module not found
```bash
# Solution: Install HODL package first
python setup.py develop
```

**Problem**: Database permission error
```bash
# Solution: Check db/ directory permissions
mkdir -p db
chmod 755 db
```

**Problem**: Database already exists
```bash
# Solution: Script will clean it automatically
# Or manually: rm db/bch.db
```

---

## Future Scripts

Potential scripts to add:

- `backup_db.sh` - Automated database backups
- `restore_db.sh` - Database restoration
- `migrate_db.py` - Database migrations
- `health_check.sh` - System health verification
- `deploy.sh` - Automated deployment
- `test_runner.sh` - Run all tests
- `benchmark.py` - Performance benchmarking

---

## Contributing

To contribute new scripts:

1. Create script in this directory
2. Make it executable
3. Test thoroughly
4. Document in this README
5. Submit pull request

See [CONTRIBUTING.md](../CONTRIBUTING.md) for detailed guidelines.

---

## Support

For issues with these scripts:
- Check [TROUBLESHOOTING.md](../TROUBLESHOOTING.md)
- Open an issue on GitHub
- Include error messages and system info

---

**These scripts make HODL setup easy! 🚀**
