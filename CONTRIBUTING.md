# Contributing to HODL

Thank you for your interest in contributing to HODL! This document provides guidelines and instructions for contributing.

## Table of Contents
1. [Code of Conduct](#code-of-conduct)
2. [Getting Started](#getting-started)
3. [Development Setup](#development-setup)
4. [Making Changes](#making-changes)
5. [Submitting Changes](#submitting-changes)
6. [Coding Standards](#coding-standards)
7. [Testing](#testing)
8. [Documentation](#documentation)

## Code of Conduct

### Our Pledge
We pledge to make participation in our project a harassment-free experience for everyone, regardless of age, body size, disability, ethnicity, sex characteristics, gender identity and expression, level of experience, education, socio-economic status, nationality, personal appearance, race, religion, or sexual identity and orientation.

### Our Standards
- Using welcoming and inclusive language
- Being respectful of differing viewpoints and experiences
- Gracefully accepting constructive criticism
- Focusing on what is best for the community
- Showing empathy towards other community members

## Getting Started

### Prerequisites
- Python 3.11 or higher
- Git
- Basic understanding of blockchain concepts
- Familiarity with Python development

### Ways to Contribute
- **Bug Reports**: Found a bug? Let us know!
- **Feature Requests**: Have an idea? Share it!
- **Code Contributions**: Fix bugs, add features
- **Documentation**: Improve or add documentation
- **Testing**: Write or improve tests
- **Reviews**: Review pull requests

## Development Setup

1. **Fork the Repository**
   ```bash
   # Click "Fork" on GitHub, then clone your fork
   git clone https://github.com/YOUR_USERNAME/hodl.git
   cd hodl
   ```

2. **Set Up Development Environment**
   ```bash
   # Run the setup script
   chmod +x scripts/setup.sh
   ./scripts/setup.sh
   
   # Or manually:
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   python setup.py develop
   ```

3. **Configure Git**
   ```bash
   git config user.name "Your Name"
   git config user.email "your.email@example.com"
   
   # Add upstream remote
   git remote add upstream https://github.com/atharv404/hodl.git
   ```

4. **Create a Branch**
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/bug-description
   ```

## Making Changes

### Branch Naming Convention
- `feature/feature-name` - New features
- `fix/bug-description` - Bug fixes
- `docs/documentation-update` - Documentation changes
- `refactor/component-name` - Code refactoring
- `test/test-description` - Test additions/improvements

### Commit Message Guidelines

Follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

**Examples:**
```bash
git commit -m "feat(wallet): add multi-signature support"
git commit -m "fix(daemon): resolve memory leak in blockchain sync"
git commit -m "docs(api): update endpoint documentation"
```

### Making Code Changes

1. **Keep Changes Focused**
   - One feature/fix per pull request
   - Keep changes small and manageable
   - Don't mix refactoring with new features

2. **Follow Python Standards**
   - Follow PEP 8 style guide
   - Use meaningful variable and function names
   - Add docstrings to functions and classes
   - Keep functions small and focused

3. **Add Tests**
   - Write tests for new features
   - Ensure existing tests still pass
   - Aim for good code coverage

4. **Update Documentation**
   - Update README if needed
   - Add/update docstrings
   - Update relevant .md files

## Submitting Changes

### Before Submitting

1. **Test Your Changes**
   ```bash
   # Run the application
   python -m hodl.daemon
   
   # Test API endpoints
   curl http://localhost:8001/status
   
   # Run tests (if available)
   pytest tests/
   ```

2. **Update Documentation**
   - Update relevant .md files
   - Add inline code comments where needed
   - Update API documentation if applicable

3. **Sync with Upstream**
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

4. **Clean Up Commits**
   ```bash
   # If you have multiple commits, consider squashing
   git rebase -i HEAD~N  # where N is number of commits
   ```

### Creating a Pull Request

1. **Push Your Branch**
   ```bash
   git push origin feature/your-feature-name
   ```

2. **Create Pull Request on GitHub**
   - Go to your fork on GitHub
   - Click "New Pull Request"
   - Select your branch
   - Fill in the PR template

3. **PR Description Should Include:**
   - **What**: What changes were made
   - **Why**: Why these changes are needed
   - **How**: How the changes were implemented
   - **Testing**: How you tested the changes
   - **Related Issues**: Link any related issues

**Example PR Description:**
```markdown
## Description
Implements multi-signature wallet support for enhanced security.

## Motivation
Users need the ability to create wallets that require multiple signatures
for transactions, improving security for high-value accounts.

## Changes
- Added MultiSigWallet class in hodl/wallet/
- Updated transaction validation logic
- Added tests for multi-sig functionality
- Updated wallet documentation

## Testing
- Created test wallets with 2-of-3 and 3-of-5 signatures
- Verified transaction signing and validation
- Tested edge cases (insufficient signatures, invalid signatures)
- All existing tests pass

## Related Issues
Closes #123
Related to #456
```

## Coding Standards

### Python Style Guide

Follow PEP 8 with these specific guidelines:

1. **Imports**
   ```python
   # Standard library imports
   import os
   import sys
   
   # Third-party imports
   from flask import Flask, jsonify
   
   # Local imports
   from hodl.block.Blockchain import Blockchain
   ```

2. **Naming Conventions**
   - Classes: `CapitalizedWords` (e.g., `Blockchain`, `Transaction`)
   - Functions/Methods: `lowercase_with_underscores` (e.g., `new_transaction`)
   - Constants: `UPPERCASE_WITH_UNDERSCORES` (e.g., `MAX_BLOCK_SIZE`)
   - Private: `_leading_underscore` (e.g., `_internal_method`)

3. **Docstrings**
   ```python
   def new_transaction(self, outs, outns, nick=''):
       """
       Create a new transaction
       
       Args:
           outs (list): List of recipient addresses
           outns (list): List of amounts corresponding to outs
           nick (str, optional): Transaction nickname. Defaults to ''.
       
       Returns:
           Transaction: The created transaction object
       
       Raises:
           NotEnoughMoney: If sender has insufficient balance
       """
       pass
   ```

4. **Line Length**
   - Maximum 100 characters per line
   - Break long lines appropriately

5. **Whitespace**
   - 4 spaces for indentation (no tabs)
   - Blank line between functions
   - Two blank lines between classes

### Code Quality

1. **Error Handling**
   ```python
   # Good
   try:
       result = risky_operation()
   except SpecificError as e:
       logger.error(f"Operation failed: {e}")
       raise
   
   # Avoid bare except
   # Bad: except:
   ```

2. **Logging**
   ```python
   import logging
   
   logger = logging.getLogger(__name__)
   logger.info("Transaction created")
   logger.error(f"Failed to process block: {error}")
   ```

3. **Type Hints** (Encouraged)
   ```python
   def process_block(block: Block) -> bool:
       """Process a blockchain block"""
       pass
   ```

## Testing

### Writing Tests

1. **Test File Structure**
   ```
   tests/
   ├── block/
   │   ├── test_block.py
   │   └── test_blockchain.py
   ├── wallet/
   │   └── test_wallet.py
   └── daemon/
       └── test_api.py
   ```

2. **Test Naming**
   ```python
   def test_create_transaction_success():
       """Test successful transaction creation"""
       pass
   
   def test_create_transaction_insufficient_funds():
       """Test transaction creation with insufficient funds"""
       pass
   ```

3. **Test Structure**
   ```python
   # Arrange
   wallet = Wallet()
   recipient = "recipient_pubkey"
   
   # Act
   transaction = wallet.new_transaction([recipient], [1.0])
   
   # Assert
   assert transaction is not None
   assert len(transaction.outs) == 1
   ```

### Running Tests

```bash
# Run all tests
pytest tests/

# Run specific test file
pytest tests/block/test_block.py

# Run with coverage
pytest --cov=hodl tests/

# Run with verbose output
pytest -v tests/
```

## Documentation

### Code Documentation

1. **Module Docstrings**
   ```python
   """
   Wallet Management Module
   
   This module provides wallet functionality including transaction creation,
   balance checking, and key management.
   """
   ```

2. **Function Docstrings** - Use Google style
   ```python
   def calculate_balance(address: str) -> float:
       """
       Calculate the balance for a given address.
       
       Args:
           address: The wallet address to check
       
       Returns:
           The balance in HDL
       
       Raises:
           ValueError: If address is invalid
       """
       pass
   ```

### Updating Documentation

When making changes, update:
- Inline code comments
- Function/class docstrings
- README.md (if changing core features)
- SETUP.md (if changing setup process)
- DEPLOYMENT.md (if affecting deployment)
- API documentation (if changing API)

## Review Process

### What to Expect

1. **Automated Checks**
   - Code syntax validation
   - Test execution
   - Style checks (if configured)

2. **Code Review**
   - Maintainer will review your code
   - May request changes
   - Discussion and iteration

3. **Approval and Merge**
   - Once approved, PR will be merged
   - Your contribution will be credited

### Responding to Feedback

- Be open to feedback
- Ask questions if unclear
- Make requested changes promptly
- Push updates to the same branch

## Recognition

Contributors are recognized in:
- Git commit history
- GitHub contributors page
- Project documentation (for significant contributions)

## Questions?

- **Documentation**: Check existing .md files
- **Issues**: Search existing issues
- **Discussion**: Open a GitHub Discussion
- **Direct Contact**: Open an issue for maintainer contact

## License

By contributing, you agree that your contributions will be licensed under the Apache 2.0 License.

---

Thank you for contributing to HODL! 🚀
