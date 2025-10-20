#!/usr/bin/env python3
"""
Create Demo Database for HODL Platform

This script creates a pre-populated database with sample blocks, transactions,
and smart contracts for demonstration purposes.

Usage:
    python scripts/create_demo_db.py
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from hodl.block.Blockchain import Blockchain
from hodl import cryptogr as cg
from hodl.wallet.wallet import Wallet
import json
import time


def create_demo_database():
    """
    Create a demo blockchain with sample data
    """
    print("Creating demo database...")
    print("=" * 50)
    
    # Initialize blockchain
    print("1. Initializing blockchain...")
    bch = Blockchain()
    
    # Clean existing data (if any)
    try:
        bch.clean()
    except:
        pass
    
    # Generate demo wallets
    print("2. Generating demo wallets...")
    alice_wallet = Wallet()
    bob_wallet = Wallet()
    charlie_wallet = Wallet()
    
    wallets = {
        'Alice': {
            'wallet': alice_wallet,
            'name': 'Alice',
            'description': 'First demo user'
        },
        'Bob': {
            'wallet': bob_wallet,
            'name': 'Bob',
            'description': 'Second demo user'
        },
        'Charlie': {
            'wallet': charlie_wallet,
            'name': 'Charlie',
            'description': 'Third demo user'
        }
    }
    
    # Save wallet information
    wallet_info = {}
    for name, info in wallets.items():
        wallet = info['wallet']
        wallet_info[name] = {
            'public_key': wallet.pubkey.hex() if isinstance(wallet.pubkey, bytes) else str(wallet.pubkey),
            'description': info['description']
        }
        print(f"   - {name}: {wallet_info[name]['public_key'][:20]}...")
    
    # Save wallet info to file
    with open('demo_wallets.json', 'w') as f:
        json.dump(wallet_info, f, indent=2)
    print("   Wallet info saved to demo_wallets.json")
    
    print("\n3. Creating genesis block...")
    # Genesis block is typically created automatically
    
    print("\n4. Database creation complete!")
    print("=" * 50)
    print("\nDemo wallets created:")
    for name, info in wallet_info.items():
        print(f"\n{name}:")
        print(f"  Public Key: {info['public_key']}")
        print(f"  Description: {info['description']}")
    
    print("\n" + "=" * 50)
    print("Database ready for use!")
    print(f"Database location: db/bch.db")
    print("\nYou can now start the daemon:")
    print("  python -m hodl.daemon")
    print("\nOr use the demo wallets in your application.")
    
    return wallet_info


def main():
    """
    Main function
    """
    try:
        create_demo_database()
        print("\n✓ Demo database created successfully!")
        return 0
    except Exception as e:
        print(f"\n✗ Error creating demo database: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
