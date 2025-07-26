# Render Quick Start Guide

Deploy your URL Shortener to Render in 5 minutes - completely free!

## Step 1: Create Render Account

1. Go to https://render.com
2. Click "Get Started for Free"
3. Sign up with your GitHub account (no credit card required)

## Step 2: Deploy Your App

1. **In Render Dashboard:**
   - Click "New +"
   - Select "Web Service"

2. **Connect Repository:**
   - Choose "Connect a repository"
   - Select your GitHub account
   - Choose your `url-shortener` repository

3. **Configure Service:**
   - **Name**: `url-shortener` (or any name you like)
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Plan**: Free

4. **Click "Create Web Service"**

## Step 3: Add Database

1. **In your project dashboard:**
   - Click "New +"
   - Select "PostgreSQL"
   - Choose "Free" plan
   - Click "Create Database"

2. **Link database to your service:**
   - Go back to your web service
   - Click "Environment"
   - Add environment variable:
     - **Key**: `DATABASE_URL`
     - **Value**: Copy from your PostgreSQL service settings

## Step 4: Test Your Deployment

Your app will be available at: `https://your-app-name.onrender.com`

### Test the endpoints:

```bash
# Health check
curl https://your-app-name.onrender.com/health

# Shorten a URL
curl -X POST "https://your-app-name.onrender.com/shorten?url=https://www.example.com"

# Check analytics
curl "https://your-app-name.onrender.com/api/stats/YOUR_SHORT_CODE"
```

### Swagger UI:
Visit: `https://your-app-name.onrender.com/docs`

## Troubleshooting

### If build fails:
1. Check Render logs in the dashboard
2. Ensure all files are committed to GitHub
3. Verify `requirements.txt` is in the root directory

### If database connection fails:
1. Verify `DATABASE_URL` is set correctly
2. Check if PostgreSQL service is running
3. Wait a few minutes for database to initialize

## Free Tier Limits

- **750 hours/month** (enough for 24/7 deployment)
- **512 MB RAM** per service
- **Shared CPU**
- **PostgreSQL database** included

## Next Steps

1. **Test all endpoints** using the Swagger UI
2. **Set up custom domain** (optional)
3. **Monitor usage** in Render dashboard
4. **Scale up** if needed (paid plans available)

## Support

- **Render Documentation**: https://render.com/docs
- **Community**: https://community.render.com/
- **Status**: https://status.render.com/

Your URL shortener will be live and accessible worldwide! 🌍 