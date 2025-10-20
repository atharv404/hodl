from setuptools import setup, find_packages
import os

# Read README for long description
def read_file(filename):
    filepath = os.path.join(os.path.dirname(__file__), filename)
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    return ''

setup(
    name='hodleum',
    version='0.1.0',
    packages=find_packages(exclude=['tests', 'tests.*', 'docs']),
    url='https://github.com/atharv404/hodl',
    license='Apache 2.0',
    author='hodleum',
    author_email='hodleum@gmail.com',
    description='HODL is a decentralized platform for payments, computing, storing and DApps',
    long_description=read_file('README.md'),
    long_description_content_type='text/markdown',
    python_requires='>=3.11',
    install_requires=[
        'flask>=3.0.0',
        'werkzeug>=3.0.0',
        'sqlalchemy>=2.0.0',
        'pycryptodome>=3.19.0',
        'attrs>=23.0.0',
        'json5>=0.9.0',
        'dpath>=2.0.0',
        'mmh3>=4.0.0',
        'coloredlogs>=15.0.0',
        'twisted>=24.0.0',
        'python-dotenv>=1.0.0',
    ],
    extras_require={
        'dev': [
            'pytest>=7.0.0',
            'pytest-cov>=4.0.0',
        ],
        'docker': [
            'docker>=7.0.0',
        ],
        'deployment': [
            'gunicorn>=21.0.0',
        ],
    },
    entry_points={
        'console_scripts': [
            'hodl-daemon=hodl.daemon:start',
        ],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Distributed Computing',
    ],
    keywords='blockchain cryptocurrency decentralized smart-contracts p2p',
    project_urls={
        'Bug Reports': 'https://github.com/atharv404/hodl/issues',
        'Source': 'https://github.com/atharv404/hodl',
        'Documentation': 'https://github.com/atharv404/hodl/blob/main/README.md',
    },
)
