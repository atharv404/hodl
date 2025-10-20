# HODL Platform - Deployment Checklist

Use this checklist to ensure a smooth deployment process.

## Pre-Deployment

### Local Development Setup
- [ ] Python 3.11+ installed
- [ ] Repository cloned
- [ ] Virtual environment created
- [ ] Dependencies installed from requirements.txt
- [ ] Database directory created (`db/`)
- [ ] Application runs locally on port 8001
- [ ] Status endpoint responding (`/status`)
- [ ] Basic API endpoints tested

### Code Preparation
- [ ] All tests passing (if applicable)
- [ ] Code linted and formatted
- [ ] No hardcoded secrets or credentials
- [ ] .env.example file created with all required variables
- [ ] .gitignore properly configured
- [ ] README updated with any project-specific notes

## Choose Your Deployment Platform

### Option A: Vercel (Serverless - Read-Only API Demo)
- [ ] `vercel.json` file present
- [ ] `api/index.py` handler created
- [ ] `api/requirements.txt` with minimal dependencies
- [ ] `.vercelignore` configured
- [ ] Vercel CLI installed (`npm i -g vercel`)
- [ ] Logged into Vercel account
- [ ] Test deployment: `vercel`
- [ ] Production deployment: `vercel --prod`
- [ ] Custom domain configured (optional)
- [ ] Environment variables set in Vercel dashboard
- [ ] HTTPS enabled (automatic with Vercel)

**Vercel Limitations:**
- ⚠️ Read-only blockchain API only
- ⚠️ No persistent SQLite storage
- ⚠️ Limited function execution time (10s default)

### Option B: Railway (Full Node - Recommended)
- [ ] `railway.json` configuration present
- [ ] `Procfile` present
- [ ] Railway CLI installed (`npm i -g @railway/cli`)
- [ ] Logged into Railway account
- [ ] Project initialized: `railway init`
- [ ] Environment variables configured
- [ ] Persistent volume configured for `db/` directory
- [ ] Deployed: `railway up`
- [ ] Custom domain configured (optional)
- [ ] HTTPS configured
- [ ] Health checks enabled
- [ ] Logs monitored: `railway logs`

**Railway Benefits:**
- ✅ Persistent storage for SQLite
- ✅ Always-on dynos
- ✅ Full blockchain node functionality
- ✅ Reasonable free tier

### Option C: Render (Full Node)
- [ ] `render.yaml` configuration present
- [ ] Account created on render.com
- [ ] New Web Service created
- [ ] Repository connected
- [ ] Build command: `pip install -r requirements.txt && python setup.py install`
- [ ] Start command: `python -m hodl.daemon`
- [ ] Environment variables configured
- [ ] Persistent disk attached (1GB+)
- [ ] Health check path set: `/status`
- [ ] Custom domain configured (optional)
- [ ] HTTPS enabled (automatic)
- [ ] Auto-deploy enabled

### Option D: Heroku (Full Node)
- [ ] `Procfile` present
- [ ] `runtime.txt` with Python version
- [ ] Heroku CLI installed
- [ ] Logged into Heroku account
- [ ] App created: `heroku create hodl-blockchain`
- [ ] PostgreSQL add-on (optional): `heroku addons:create heroku-postgresql:mini`
- [ ] Environment variables set: `heroku config:set VAR=value`
- [ ] Deployed: `git push heroku main`
- [ ] Dynos scaled: `heroku ps:scale web=1`
- [ ] Logs checked: `heroku logs --tail`
- [ ] Custom domain configured (optional)

### Option E: Docker (Any Platform)
- [ ] `Dockerfile` present and tested
- [ ] `docker-compose.yml` configured
- [ ] Docker installed locally
- [ ] Image builds successfully: `docker-compose build`
- [ ] Container runs locally: `docker-compose up`
- [ ] Volumes configured for persistent data
- [ ] Health check working
- [ ] Logs accessible: `docker-compose logs`
- [ ] Production environment variables set
- [ ] Image pushed to registry (if applicable)
- [ ] Deployed to production environment
- [ ] Monitoring configured

### Option F: Traditional VPS (Full Control)
- [ ] VPS provisioned (DigitalOcean, AWS EC2, etc.)
- [ ] SSH access configured
- [ ] Python 3.11+ installed on server
- [ ] SQLite installed on server
- [ ] Repository cloned on server
- [ ] Virtual environment created
- [ ] Dependencies installed
- [ ] Systemd service file created (`/etc/systemd/system/hodl.service`)
- [ ] Service enabled: `systemctl enable hodl`
- [ ] Service started: `systemctl start hodl`
- [ ] Nginx installed and configured
- [ ] Reverse proxy configured
- [ ] SSL certificate installed (Let's Encrypt)
- [ ] Firewall configured (UFW/iptables)
- [ ] Automatic backups scheduled

## Security Configuration

### Environment Variables
- [ ] `SECRET_KEY` set to strong random value
- [ ] `DATABASE_URL` configured (if using PostgreSQL)
- [ ] `FLASK_ENV` set to `production`
- [ ] `FLASK_DEBUG` set to `False`
- [ ] API keys and secrets not in code
- [ ] `.env` file added to `.gitignore`

### SSL/HTTPS
- [ ] HTTPS enabled on production domain
- [ ] HTTP to HTTPS redirect configured
- [ ] SSL certificate valid and not expired
- [ ] HSTS headers enabled (if applicable)

### API Security
- [ ] CORS configured properly (not `*` in production)
- [ ] Rate limiting implemented (optional but recommended)
- [ ] Input validation on all endpoints
- [ ] SQL injection prevention (SQLAlchemy handles this)
- [ ] XSS prevention

### Access Control
- [ ] Firewall rules configured
- [ ] SSH keys only (no password auth for VPS)
- [ ] Database not exposed to internet
- [ ] Admin interfaces protected
- [ ] Monitoring alerts configured

## Post-Deployment

### Verification
- [ ] Application accessible via production URL
- [ ] `/status` endpoint returns 200 OK
- [ ] `/get_block/0` returns genesis block
- [ ] All API endpoints functional
- [ ] No errors in application logs
- [ ] Database persisting correctly
- [ ] Health checks passing

### Monitoring Setup
- [ ] Application logs configured
- [ ] Error tracking enabled (Sentry, Rollbar, etc.)
- [ ] Uptime monitoring enabled (UptimeRobot, Pingdom)
- [ ] Performance monitoring (optional)
- [ ] Log aggregation (Papertrail, Loggly, etc.)
- [ ] Alert notifications configured
- [ ] Status page created (optional)

### Backup Strategy
- [ ] Database backup script created
- [ ] Automated daily backups scheduled
- [ ] Backup retention policy defined
- [ ] Backup restoration tested
- [ ] Off-site backup storage configured
- [ ] Backup monitoring/alerts enabled

### Documentation
- [ ] Deployment process documented
- [ ] Environment variables documented
- [ ] Runbook for common operations
- [ ] Incident response plan
- [ ] Team access credentials secured
- [ ] API documentation published (optional)

### Performance Optimization
- [ ] Application response times acceptable
- [ ] Database queries optimized
- [ ] Caching implemented (if needed)
- [ ] Static assets served efficiently
- [ ] CDN configured (optional)
- [ ] Load testing performed (optional)

## Ongoing Maintenance

### Regular Tasks
- [ ] Monitor application logs daily
- [ ] Check error rates weekly
- [ ] Review security alerts
- [ ] Update dependencies monthly
- [ ] Verify backups weekly
- [ ] Review disk space usage
- [ ] Check SSL certificate expiration
- [ ] Monitor API usage/costs

### Updates & Patches
- [ ] Process for applying security patches
- [ ] Process for dependency updates
- [ ] Testing procedure before production updates
- [ ] Rollback plan if updates fail
- [ ] Changelog maintained

### Scaling Considerations
- [ ] Monitor resource usage (CPU, RAM, disk)
- [ ] Plan for horizontal scaling if needed
- [ ] Database scaling strategy
- [ ] Load balancer setup (if needed)
- [ ] Cache layer (Redis/Memcached) if needed

## Platform-Specific Notes

### Vercel
- Monitor function execution time (10s limit)
- Check serverless function invocations
- Review bandwidth usage
- Static files cached at edge

### Railway
- Monitor disk usage (persistent volume)
- Check memory usage (crashes if exceeded)
- Review build logs for issues
- Restart app if needed via dashboard

### Heroku
- Keep dyno awake (free tier sleeps after 30 min)
- Monitor dyno hours (free tier limited)
- PostgreSQL row limits (if using free tier)
- Review app metrics in dashboard

### Docker
- Prune old images regularly: `docker system prune`
- Monitor container resource usage
- Update base images for security patches
- Check logs: `docker-compose logs -f`

### VPS
- Keep OS updated: `apt update && apt upgrade`
- Monitor disk space: `df -h`
- Check service status: `systemctl status hodl`
- Review system logs: `journalctl -u hodl -f`
- Nginx logs: `/var/log/nginx/`

## Troubleshooting

If issues arise post-deployment, refer to:
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for common issues
- Application logs for specific errors
- Platform status pages for service outages
- Community support channels

## Support Contacts

- **GitHub Issues**: https://github.com/atharv404/hodl/issues
- **Documentation**: See SETUP.md, DEPLOYMENT.md, TROUBLESHOOTING.md
- **Platform Support**:
  - Vercel: https://vercel.com/support
  - Railway: https://railway.app/help
  - Render: https://render.com/docs
  - Heroku: https://help.heroku.com

---

## Deployment Completion

Once all applicable items are checked, your HODL node is production-ready! 🎉

**Congratulations on deploying HODL!**

Remember to:
- Keep documentation updated
- Monitor regularly
- Backup frequently
- Update dependencies
- Stay secure

For questions or issues, open an issue on GitHub or consult the documentation.
