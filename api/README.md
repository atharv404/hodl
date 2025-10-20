# HODL Platform - Serverless API

This directory contains the serverless API implementation for deploying HODL as a read-only blockchain explorer on Vercel and similar serverless platforms.

## Overview

The serverless API provides a lightweight, read-only REST API for querying blockchain data. It's designed for:
- Quick demos and presentations
- Public blockchain explorers
- Educational purposes
- Testing and development

**Note**: This is a **read-only API**. For full blockchain node functionality (transactions, mining, smart contracts), deploy to Railway, Render, or a traditional server.

## Files

### index.py
Main serverless function handler that implements the Flask API.

**Endpoints**:
- `GET /` - API home with endpoint documentation
- `GET /api/status` - API status and information
- `GET /api/info` - Blockchain general information
- `GET /api/block/<index>` - Get block by index (demo data)
- `GET /api/stats` - Blockchain statistics (demo data)
- `GET /api/health` - Health check endpoint

**Features**:
- CORS enabled for cross-origin requests
- Error handling with proper HTTP status codes
- JSON responses
- Demo data for testing (modify for production)

### requirements.txt
Minimal dependencies for serverless deployment:
- Flask 3.1.2
- Werkzeug 3.1.3

**Why minimal?**
Serverless platforms have size limits (typically 50MB). We include only essential packages to stay under the limit.

## Deployment

### Vercel (Recommended)

1. **Install Vercel CLI**:
```bash
npm i -g vercel
```

2. **Login to Vercel**:
```bash
vercel login
```

3. **Deploy**:
```bash
# From project root
vercel --prod
```

Your API will be live at: `https://your-project.vercel.app`

### Configuration

The `vercel.json` file in the project root configures:
- Python runtime
- Build settings
- Routing rules
- Environment variables
- Function settings (memory, timeout)

## Using the API

Once deployed, test your endpoints:

### Check Status
```bash
curl https://your-project.vercel.app/api/status
```

**Response**:
```json
{
  "status": "online",
  "version": "0.1",
  "mode": "read-only",
  "platform": "vercel-serverless"
}
```

### Get Block
```bash
curl https://your-project.vercel.app/api/block/0
```

### Get Stats
```bash
curl https://your-project.vercel.app/api/stats
```

### API Documentation
```bash
curl https://your-project.vercel.app/
```

## Customization

### Adding Real Blockchain Data

To connect to a real blockchain database instead of demo data:

1. **Update index.py**:
```python
# Uncomment these lines in get_block()
from hodl.block.Blockchain import Blockchain
bch = Blockchain(m='ro')
block = bch[index]
return jsonify({'block': str(block), 'index': index})
```

2. **Update requirements.txt**:
```
flask>=3.0.0
werkzeug>=3.0.0
sqlalchemy>=2.0.0
pycryptodome>=3.19.0
attrs>=23.0.0
```

3. **Include database**:
   - Pre-populate `db/bch.db` locally
   - Include it in deployment (remove from `.vercelignore`)

**Warning**: Vercel's filesystem is read-only, so blockchain data won't update. For a full node, use Railway or Render instead.

### Adding New Endpoints

Add new endpoints to `index.py`:

```python
@app.route('/api/transaction/<string:tx_id>')
def get_transaction(tx_id):
    """Get transaction by ID"""
    try:
        # Your logic here
        return jsonify({'transaction': 'data'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
```

### Custom Domain

In Vercel dashboard:
1. Go to your project
2. Settings → Domains
3. Add your custom domain
4. Update DNS records

## Limitations

### Vercel Serverless Constraints

- ⚠️ **Read-only**: No write operations to database
- ⚠️ **Execution Time**: 10 seconds default (60s max on Pro)
- ⚠️ **Memory**: 1024 MB default (3GB max on Pro)
- ⚠️ **Size**: 50 MB function size limit
- ⚠️ **Cold Starts**: First request may be slow
- ⚠️ **No WebSockets**: HTTP only
- ⚠️ **No Long Processes**: Functions timeout after limit

### What This API CAN'T Do

- ❌ Process transactions
- ❌ Mine blocks
- ❌ Execute smart contracts
- ❌ Update blockchain data
- ❌ Real-time updates
- ❌ WebSocket connections

### What This API CAN Do

- ✅ Query existing blocks
- ✅ Display blockchain statistics
- ✅ Provide API documentation
- ✅ Serve as blockchain explorer
- ✅ Demo blockchain concepts
- ✅ Educational purposes

## Alternative Platforms

If Vercel doesn't meet your needs:

### Netlify Functions
Similar to Vercel with comparable limitations.

**Deploy**:
```bash
npm i -g netlify-cli
netlify deploy --prod
```

### AWS Lambda
More configuration required but very scalable.

**Deploy**:
Use Serverless Framework or AWS SAM.

### Google Cloud Functions
Similar to AWS Lambda with Google's infrastructure.

**Deploy**:
```bash
gcloud functions deploy hodl-api --runtime python311 --trigger-http
```

## Full Node Deployment

For a complete blockchain node with all features:

### Railway (Recommended)
```bash
railway up
```
- ✅ Persistent storage
- ✅ Always on
- ✅ Full features

### Render
```bash
# Deploy via dashboard or render.yaml
```
- ✅ Persistent disk
- ✅ Free tier
- ✅ Full features

### Docker
```bash
docker-compose up -d
```
- ✅ Full control
- ✅ All features
- ✅ Any platform

See [DEPLOYMENT.md](../DEPLOYMENT.md) for detailed instructions.

## Development

### Local Testing

Test the serverless API locally:

```bash
cd api
python index.py
```

The API will run on `http://localhost:5000`

### Testing Endpoints

```bash
# Status
curl http://localhost:5000/api/status

# Block
curl http://localhost:5000/api/block/0

# Stats
curl http://localhost:5000/api/stats
```

## Monitoring

### Vercel Dashboard

Monitor your deployment:
- Request count
- Error rate
- Function execution time
- Bandwidth usage

### Adding Analytics

Add analytics to track API usage:

```python
@app.before_request
def log_request():
    """Log each request"""
    print(f"Request: {request.method} {request.path}")
```

### Error Tracking

Integrate Sentry for error tracking:

```python
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

sentry_sdk.init(
    dsn="your-sentry-dsn",
    integrations=[FlaskIntegration()]
)
```

## Performance

### Optimization Tips

1. **Minimize Dependencies**: Keep requirements.txt minimal
2. **Cache Responses**: Use caching for frequently accessed data
3. **Optimize Queries**: Index database fields
4. **Compress Responses**: Enable gzip compression
5. **CDN**: Use Vercel's built-in CDN

### Caching Example

```python
from functools import lru_cache

@lru_cache(maxsize=100)
def get_block_cached(index):
    """Cached block retrieval"""
    return get_block_from_db(index)
```

## Security

### Best Practices

1. **CORS**: Configure properly (not `*` in production)
2. **Rate Limiting**: Implement to prevent abuse
3. **Input Validation**: Validate all inputs
4. **Error Handling**: Don't leak sensitive info
5. **HTTPS**: Always use HTTPS (automatic on Vercel)

### Environment Variables

Set in Vercel dashboard:
```
SECRET_KEY=your-secret-key
API_KEY=your-api-key
```

Access in code:
```python
import os
secret = os.environ.get('SECRET_KEY')
```

## Troubleshooting

### Function Size Too Large
- Reduce dependencies in requirements.txt
- Remove unused imports
- Use minimal packages

### Timeout Errors
- Optimize queries
- Reduce processing time
- Consider upgrading to Pro plan

### Import Errors
- Check requirements.txt
- Verify package compatibility
- Test locally first

### CORS Issues
- Check CORS configuration
- Verify allowed origins
- Test with curl

See [TROUBLESHOOTING.md](../TROUBLESHOOTING.md) for more help.

## Resources

### Documentation
- [Vercel Python Docs](https://vercel.com/docs/runtimes#official-runtimes/python)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [HODL Deployment Guide](../DEPLOYMENT.md)

### Examples
- Vercel Python Examples: https://github.com/vercel/examples/tree/main/python
- Flask API Examples: https://flask.palletsprojects.com/en/latest/

## Support

For issues with the serverless API:
- Check [TROUBLESHOOTING.md](../TROUBLESHOOTING.md)
- Review Vercel function logs
- Open an issue on GitHub

---

**Happy deploying! 🚀**
