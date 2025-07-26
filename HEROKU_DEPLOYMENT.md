# Heroku Deployment Guide

This guide will walk you through deploying your URL Shortener to Heroku using Docker.

## Prerequisites

1. **Heroku CLI** installed
2. **Git** repository initialized
3. **Heroku account** (free tier available)

## Step-by-Step Deployment

### 1. **Install Heroku CLI** (if not already installed)

```bash
# macOS
brew tap heroku/brew && brew install heroku

# Windows
# Download from: https://devcenter.heroku.com/articles/heroku-cli

# Linux
curl https://cli-assets.heroku.com/install.sh | sh
```

### 2. **Login to Heroku**

```bash
heroku login
```

### 3. **Initialize Git** (if not already done)

```bash
git init
git add .
git commit -m "Initial commit for Heroku deployment"
```

### 4. **Create Heroku App**

```bash
# Create a new Heroku app
heroku create your-url-shortener-app

# Or use a random name
heroku create
```

### 5. **Add PostgreSQL Database** (Recommended)

```bash
# Add PostgreSQL addon
heroku addons:create heroku-postgresql:mini

# Verify the database URL
heroku config:get DATABASE_URL
```

### 6. **Set Buildpack** (if needed)

```bash
# Set the container stack
heroku stack:set container
```

### 7. **Deploy to Heroku**

```bash
# Push to Heroku
git push heroku main

# Or if you're on master branch
git push heroku master
```

### 8. **Open Your App**

```bash
# Open in browser
heroku open

# Or get the URL
heroku info -s | grep web_url
```

## Environment Variables

Your app will automatically use these environment variables:

- `DATABASE_URL`: Automatically set by Heroku PostgreSQL addon
- `PORT`: Automatically set by Heroku

## Verify Deployment

### 1. **Check App Status**

```bash
heroku ps
```

### 2. **View Logs**

```bash
heroku logs --tail
```

### 3. **Test Your API**

```bash
# Get your app URL
APP_URL=$(heroku info -s | grep web_url | cut -d= -f2)

# Test health endpoint
curl $APP_URL/health

# Test URL shortening
curl -X POST "$APP_URL/shorten?url=https://www.example.com"
```

## Troubleshooting

### Common Issues

1. **Build Fails**
   ```bash
   # Check build logs
   heroku logs --tail
   
   # Ensure all files are committed
   git status
   git add .
   git commit -m "Fix build issues"
   git push heroku main
   ```

2. **Database Connection Issues**
   ```bash
   # Check database URL
   heroku config:get DATABASE_URL
   
   # Restart the app
   heroku restart
   ```

3. **Port Issues**
   - The app automatically uses Heroku's `$PORT` environment variable
   - No manual configuration needed

### Useful Commands

```bash
# View app info
heroku info

# Check environment variables
heroku config

# Restart the app
heroku restart

# Scale the app (if needed)
heroku ps:scale web=1

# View recent logs
heroku logs --tail

# Run one-off commands
heroku run python -c "print('Hello from Heroku!')"
```

## Production Considerations

### 1. **Database Migration**

If you need to run database migrations:

```bash
heroku run python -c "from app.models import Base; from app.main import engine; Base.metadata.create_all(bind=engine)"
```

### 2. **Custom Domain** (Optional)

```bash
# Add custom domain
heroku domains:add yourdomain.com

# Configure DNS as instructed
```

### 3. **Monitoring**

```bash
# Add monitoring addon
heroku addons:create papertrail:choklad
```

## Cost Optimization

- **Free Tier**: No longer available on Heroku
- **Eco Dyno**: $5/month for basic usage
- **Basic Dyno**: $7/month for better performance

## Security Notes

1. **Environment Variables**: Never commit sensitive data
2. **CORS**: Configure `allow_origins` for production
3. **Rate Limiting**: Already implemented in the app
4. **Logging**: Monitor logs for suspicious activity

## Next Steps

After successful deployment:

1. **Test all endpoints** using the Swagger UI at `https://your-app.herokuapp.com/docs`
2. **Set up monitoring** with Heroku addons
3. **Configure custom domain** if needed
4. **Set up CI/CD** with GitHub Actions

## Support

- **Heroku Documentation**: https://devcenter.heroku.com/
- **Heroku Status**: https://status.heroku.com/
- **Community**: https://devcenter.heroku.com/articles/support-channels 