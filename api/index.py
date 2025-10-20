"""
HODL Blockchain Explorer API for Vercel Serverless Deployment

This is a read-only blockchain explorer API designed to run on Vercel.
For full node functionality with mining and transactions, deploy to a platform
with persistent storage (Railway, Render, or traditional VPS).

Author: HODL Development Team
License: Apache 2.0
"""

from flask import Flask, jsonify, request
import os
import sys
import json

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

app = Flask(__name__)

# Enable CORS for demo purposes
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response


@app.route('/')
def home():
    """
    API home page with available endpoints
    """
    return jsonify({
        'name': 'HODL Blockchain Explorer API',
        'version': '0.1',
        'status': 'online',
        'mode': 'read-only',
        'description': 'HODL is a decentralized platform for payments, computing, storing and DApps',
        'endpoints': {
            'status': {
                'path': '/api/status',
                'method': 'GET',
                'description': 'Get API status and info'
            },
            'block': {
                'path': '/api/block/<index>',
                'method': 'GET',
                'description': 'Get block by index',
                'example': '/api/block/0'
            },
            'stats': {
                'path': '/api/stats',
                'method': 'GET',
                'description': 'Get blockchain statistics'
            },
            'info': {
                'path': '/api/info',
                'method': 'GET',
                'description': 'Get blockchain information'
            }
        },
        'documentation': 'https://github.com/atharv404/hodl',
        'original_project': 'https://github.com/hodleum/hodl',
        'note': 'This is a demo API. For full node functionality, deploy to Railway, Render, or VPS.'
    })


@app.route('/api/status')
def status():
    """
    Get API status
    """
    return jsonify({
        'status': 'online',
        'version': '0.1',
        'mode': 'read-only',
        'platform': 'vercel-serverless',
        'python_version': f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
        'features': {
            'blockchain_query': True,
            'transaction_submission': False,
            'mining': False,
            'smart_contracts': False
        },
        'note': 'Read-only API for demonstration purposes'
    })


@app.route('/api/info')
def info():
    """
    Get blockchain general information
    """
    return jsonify({
        'name': 'HODL',
        'description': 'HODL is a decentralized platform for payments, computing, storing and DApps',
        'features': [
            'Smart Contracts in Python',
            'Decentralized Computing',
            'Decentralized Storage',
            'Proof-of-Work and Proof-of-Stake Mining',
            'Decentralized Internet (HDI)'
        ],
        'blockchain': {
            'consensus': 'PoW + PoS Hybrid',
            'smart_contract_language': 'Python 3',
            'block_time': 'Variable',
            'network': 'testnet'
        },
        'technology': {
            'database': 'SQLite',
            'api': 'Flask REST',
            'cryptography': 'pycryptodome'
        }
    })


@app.route('/api/block/<int:index>')
def get_block(index):
    """
    Get block by index
    
    Note: This is a demo endpoint. In production, this would query
    the actual blockchain database.
    """
    try:
        # In production, this would query the blockchain:
        # from hodl.block.Blockchain import Blockchain
        # bch = Blockchain(m='ro')
        # block = bch[index]
        
        # For demo, return mock data
        if index < 0:
            return jsonify({'error': 'Invalid block index'}), 400
        
        # Demo response
        return jsonify({
            'index': index,
            'hash': f'0x{"0" * 63}{index}',
            'timestamp': 1640000000 + (index * 600),
            'transactions': [],
            'smart_contracts': [],
            'note': 'This is demo data. Deploy with database for real blockchain data.'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/stats')
def stats():
    """
    Get blockchain statistics
    """
    return jsonify({
        'blockchain': {
            'total_blocks': 0,
            'total_transactions': 0,
            'total_smart_contracts': 0
        },
        'network': {
            'status': 'demo',
            'peers': 0,
            'difficulty': 1000000
        },
        'note': 'This is a demo API. Statistics shown are placeholders.'
    })


@app.route('/api/health')
def health():
    """
    Health check endpoint for monitoring
    """
    return jsonify({
        'status': 'healthy',
        'timestamp': __import__('time').time()
    })


@app.errorhandler(404)
def not_found(error):
    """
    Handle 404 errors
    """
    return jsonify({
        'error': 'Endpoint not found',
        'status': 404,
        'available_endpoints': [
            '/',
            '/api/status',
            '/api/info',
            '/api/block/<index>',
            '/api/stats',
            '/api/health'
        ]
    }), 404


@app.errorhandler(500)
def internal_error(error):
    """
    Handle 500 errors
    """
    return jsonify({
        'error': 'Internal server error',
        'status': 500,
        'message': str(error)
    }), 500


# For local testing
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
