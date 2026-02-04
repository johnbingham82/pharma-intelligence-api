# Deploy Pharma Intelligence API to AWS App Runner
## ⚡ Fastest & Easiest AWS Deployment (Baby Steps)

**Why App Runner?**
- ✅ Takes your Dockerfile directly
- ✅ Automatic HTTPS
- ✅ Automatic scaling
- ✅ Fast performance
- ✅ Pay only for what you use
- ✅ ~$5-10/month for low traffic

**Total Time:** ~10-15 minutes

---

## 📋 Prerequisites

### What You Need:
1. **AWS Account** (free tier available)
2. **Credit card** (for AWS account - free tier covers most costs)
3. **Your computer** with internet

### What You DON'T Need:
- ❌ Docker installed locally
- ❌ AWS CLI installed
- ❌ Complex configurations
- ❌ DevOps knowledge

---

## 🚀 Step-by-Step Deployment

### STEP 1: Create AWS Account (5 minutes)

**1.1** Go to: https://aws.amazon.com

**1.2** Click **"Create an AWS Account"** (orange button, top right)

**1.3** Fill in:
- Email address
- AWS account name (e.g., "PharmaIntel")
- Click **Continue**

**1.4** Create password:
- Root user password
- Confirm password
- Click **Continue**

**1.5** Contact information:
- Choose **"Personal"** (unless you're a company)
- Full name
- Phone number
- Country
- Address
- Click **Continue**

**1.6** Payment information:
- Add credit card (required but won't charge unless you exceed free tier)
- Click **Verify and Continue**

**1.7** Identity verification:
- Choose SMS or Voice call
- Enter code you receive
- Click **Continue**

**1.8** Choose support plan:
- Select **"Basic support - Free"**
- Click **Complete sign up**

**1.9** Wait for email confirmation (~2 minutes)

✅ **AWS account is now ready!**

---

### STEP 2: Sign in to AWS Console (1 minute)

**2.1** Go to: https://console.aws.amazon.com

**2.2** Click **"Sign in to the Console"**

**2.3** Select **"Root user"**

**2.4** Enter your email and password

**2.5** Click **"Sign in"**

✅ **You're now in the AWS Console!**

---

### STEP 3: Push Code to GitHub (3 minutes)

**Why?** App Runner needs to access your code from GitHub.

**3.1** If you don't have a GitHub account:
- Go to: https://github.com/signup
- Create account (takes 2 minutes)

**3.2** Create a new repository:
- Go to: https://github.com/new
- Repository name: `pharma-intelligence-api`
- Make it **Public** (easier for first deployment)
- Click **"Create repository"**

**3.3** Push your code to GitHub:

```bash
# In your project directory
cd /Users/administrator/.openclaw/workspace

# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit - Pharma Intelligence API"

# Add remote (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/pharma-intelligence-api.git

# Push
git push -u origin main
```

**If it asks for credentials:**
- Username: Your GitHub username
- Password: Create a Personal Access Token:
  1. Go to: https://github.com/settings/tokens
  2. Click **"Generate new token (classic)"**
  3. Select **"repo"** scope
  4. Click **"Generate token"**
  5. Copy the token and use it as password

✅ **Code is now on GitHub!**

---

### STEP 4: Create AWS App Runner Service (5 minutes)

**4.1** In AWS Console, search for **"App Runner"** in the top search bar

**4.2** Click **"App Runner"** in the results

**4.3** Click **"Create service"** (big orange button)

---

#### Screen 1: Source

**4.4** Choose source:
- Select **"Source code repository"**
- Click **"Add new"** next to GitHub

**4.5** Connect GitHub:
- A popup will open
- Click **"Authorize AWS Connector for GitHub"**
- Sign in to GitHub if asked
- Click **"Authorize"**
- Select **"All repositories"** or just your `pharma-intelligence-api` repo
- Click **"Install"**
- Close the popup

**4.6** Repository settings:
- Repository: Select `your-username/pharma-intelligence-api`
- Branch: `main`
- Deployment trigger: **"Automatic"** (deploys on every push)
- Click **"Next"**

---

#### Screen 2: Build Settings

**4.7** Configure build:
- Build method: **"Dockerfile"**
- Dockerfile path: `api/Dockerfile`
- Dockerfile context: `.` (root directory)

**4.8** Click **"Next"**

---

#### Screen 3: Service Settings

**4.9** Service name:
- Enter: `pharma-intelligence-api`

**4.10** Virtual CPU and memory:
- Choose **"1 vCPU"** and **"2 GB"** (good for starting)
- (You can change this later)

**4.11** Environment variables:
- Click **"Add environment variable"**
- Add these:

| Key | Value |
|-----|-------|
| `ENV` | `production` |
| `CORS_ORIGINS` | `https://your-frontend-url.com,http://localhost:3000` |

**For now, just add:**
- Key: `ENV`
- Value: `production`

(You can add CORS_ORIGINS after you know your frontend URL)

**4.12** Port:
- Port: `8000` (this is what our API uses)

**4.13** Health check:
- Protocol: `HTTP`
- Path: `/health`
- Interval: `20` seconds
- Timeout: `5` seconds
- Unhealthy threshold: `3`
- Healthy threshold: `2`

**4.14** Auto scaling:
- Max concurrency: `100` (requests per instance)
- Min size: `1` (always have 1 instance running)
- Max size: `3` (scale up to 3 instances if needed)

**4.15** Click **"Next"**

---

#### Screen 4: Review

**4.16** Review everything:
- Check all settings
- **Estimated cost:** ~$12-25/month
  - (Includes free tier: 1 million requests/month, 720 hours compute)
  - Actual cost will be lower with free tier

**4.17** Click **"Create & Deploy"**

---

### STEP 5: Wait for Deployment (5-10 minutes)

**5.1** You'll see the deployment status page

**5.2** Status will show:
- ⏳ **"Operation in progress"** (yellow)
- This takes 5-10 minutes

**5.3** Watch the logs (optional):
- Click **"Logs"** tab
- See the build progress

**5.4** When complete, status will change to:
- ✅ **"Running"** (green)

**5.5** Copy your API URL:
- Look for **"Default domain"**
- Will be something like: `https://abc123xyz.us-east-1.awsapprunner.com`
- **COPY THIS URL** - you'll need it!

✅ **API is now deployed and running!**

---

### STEP 6: Test Your API (2 minutes)

**6.1** Test health endpoint:

Open your browser or use terminal:

```bash
# Replace with YOUR API URL
curl https://YOUR-URL.awsapprunner.com/health
```

**Expected response:**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "timestamp": "2026-02-04T13:45:00Z",
  "data_sources": {
    "UK": "available",
    "US": "available",
    "AU": "available",
    ...
  }
}
```

**6.2** Test API docs:

Open in browser:
```
https://YOUR-URL.awsapprunner.com/docs
```

You should see the interactive API documentation!

**6.3** Test a real endpoint:

```bash
# Get Australia data
curl https://YOUR-URL.awsapprunner.com/api/country/au
```

✅ **API is working!**

---

### STEP 7: Connect Frontend to API (2 minutes)

**7.1** Update frontend configuration:

Create file: `frontend/src/config.ts`

```typescript
export const API_BASE_URL = import.meta.env.PROD
  ? 'https://YOUR-URL.awsapprunner.com'  // Replace with YOUR URL
  : 'http://localhost:8000'
```

**7.2** Use in API calls:

Update any file that makes API calls:

```typescript
import { API_BASE_URL } from './config'

// Instead of:
// const response = await fetch('http://localhost:8000/api/...')

// Use:
const response = await fetch(`${API_BASE_URL}/api/...`)
```

**7.3** Update CORS in AWS:

Go back to App Runner console:
- Click your service
- Click **"Configuration"** tab
- Click **"Edit"** in Environment variables
- Add or update `CORS_ORIGINS`:
  - Value: `https://your-frontend-url.com,http://localhost:3000`
- Click **"Save changes"**
- Wait 2-3 minutes for redeployment

✅ **Frontend is now connected to AWS API!**

---

## 🎉 You're Done!

### What You Have Now:
- ✅ API running on AWS App Runner
- ✅ Automatic HTTPS
- ✅ Automatic scaling (1-3 instances)
- ✅ Automatic deployments (on GitHub push)
- ✅ Health monitoring
- ✅ Production-ready

### Your API URLs:
- **API Base:** https://YOUR-URL.awsapprunner.com
- **Health Check:** https://YOUR-URL.awsapprunner.com/health
- **API Docs:** https://YOUR-URL.awsapprunner.com/docs
- **Countries:** https://YOUR-URL.awsapprunner.com/api/countries

---

## 💰 Costs (Important!)

### Free Tier (First 12 months):
- **2,000 build minutes/month** - FREE
- **2 GB storage** - FREE
- **You'll likely stay in free tier!**

### After Free Tier:
- **Compute:** ~$0.007/hour per vCPU = ~$5/month for 1 vCPU
- **Memory:** ~$0.0008/hour per GB = ~$0.50/month for 2 GB
- **Requests:** FREE (unlimited in App Runner)
- **Total:** ~$5-12/month for small traffic

### How to Reduce Costs:
1. **Pause service** when not using:
   - App Runner → Select service → Actions → Pause service
   - Costs drop to $0

2. **Delete service** if done testing:
   - App Runner → Select service → Actions → Delete service

---

## 🔧 Common Issues & Fixes

### Issue 1: Build Fails

**Symptom:** Deployment stuck or fails during build

**Fix:**
1. Check Dockerfile path is correct: `api/Dockerfile`
2. Check logs in App Runner console
3. Verify all files are pushed to GitHub

### Issue 2: Service Unhealthy

**Symptom:** Status shows "Unhealthy"

**Fix:**
1. Check health endpoint: `/health`
2. Verify port is `8000`
3. Check logs for errors

### Issue 3: CORS Errors

**Symptom:** Frontend can't connect to API

**Fix:**
1. Add CORS_ORIGINS environment variable
2. Include your frontend URL
3. Redeploy (automatic after env var change)

### Issue 4: Data Sources Not Loading

**Symptom:** API works but returns empty data

**Fix:**
1. Check if `pbs_data` folder is in GitHub repo
2. Check if data source files are pushed
3. Verify file paths in code

---

## 📊 Monitoring Your API

### View Logs:
1. Go to App Runner console
2. Click your service
3. Click **"Logs"** tab
4. See real-time logs

### View Metrics:
1. Click **"Metrics"** tab
2. See:
   - Requests per minute
   - Response times
   - Error rates
   - CPU/Memory usage

### Set Up Alarms:
1. Click **"Alarms"** tab
2. Create alarm for:
   - High error rate
   - Slow response time
   - High CPU usage

---

## 🚀 Advanced: Custom Domain (Optional)

### Add Your Own Domain:

**1. Purchase domain** (GoDaddy, Namecheap, AWS Route53)

**2. In App Runner:**
- Click **"Custom domains"** tab
- Click **"Link domain"**
- Enter your domain
- Follow DNS verification steps

**3. Update CORS:**
- Add your domain to CORS_ORIGINS
- Redeploy

---

## 🔄 Deploy Updates

### Automatic Deployment:
Every time you push to GitHub `main` branch, App Runner automatically:
1. Pulls new code
2. Builds new Docker image
3. Deploys new version
4. Zero downtime!

### Manual Deployment:
1. Go to App Runner console
2. Click your service
3. Click **"Deploy"** button
4. Wait 5 minutes

---

## 📝 Checklist

- [x] AWS account created
- [x] Signed in to AWS Console
- [x] Code pushed to GitHub
- [x] App Runner service created
- [x] API deployed and running
- [x] Health check passing
- [x] API tested
- [x] Frontend connected
- [x] CORS configured
- [ ] Custom domain (optional)
- [ ] Monitoring set up
- [ ] Costs monitored

---

## 🎯 Next Steps

1. **Test all endpoints** in your frontend
2. **Monitor costs** in AWS Billing dashboard
3. **Set up CloudWatch alarms** for errors
4. **Add authentication** (future)
5. **Deploy frontend** to AWS Amplify or Vercel

---

## 📞 Need Help?

### Check Status:
- App Runner Console: https://console.aws.amazon.com/apprunner
- Service logs for errors
- Health endpoint for API status

### AWS Support:
- Free tier includes basic support
- AWS documentation: https://docs.aws.amazon.com/apprunner/

### Common URLs:
- AWS Console: https://console.aws.amazon.com
- App Runner: https://console.aws.amazon.com/apprunner
- Billing: https://console.aws.amazon.com/billing

---

## 💡 Pro Tips

1. **Use GitHub Actions** for CI/CD testing before deployment

2. **Enable auto-pause** to save money:
   - Service pauses after 5 minutes of no traffic
   - Auto-resumes on first request

3. **Monitor billing** weekly:
   - Set up billing alerts
   - Check AWS Cost Explorer

4. **Backup strategy**:
   - All code is in GitHub (already backed up!)
   - Download logs periodically if needed

---

## ✅ Success Criteria

You've succeeded when:
- ✅ You can access https://YOUR-URL.awsapprunner.com/health
- ✅ You can see API docs at /docs
- ✅ Frontend can make requests to API
- ✅ No CORS errors
- ✅ All data sources loading
- ✅ Response time < 500ms

---

**🎉 Congratulations! Your API is live on AWS!**

**Your API:** https://YOUR-URL.awsapprunner.com
**Cost:** ~$5-12/month (likely FREE for first year)
**Speed:** Global CDN, automatic scaling
**Maintenance:** Automatic updates from GitHub

---

**Created:** 2026-02-04
**Method:** AWS App Runner
**Difficulty:** ⭐ Easiest AWS option
**Speed:** ⚡ Very fast with auto-scaling
