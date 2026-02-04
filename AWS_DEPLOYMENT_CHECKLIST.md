# AWS App Runner Deployment - Quick Checklist

## ✅ Pre-Deployment Checklist

### Before You Start:
- [ ] Have a valid email address
- [ ] Have a credit card (for AWS account)
- [ ] Have GitHub account (or willing to create one)
- [ ] Code is ready in workspace directory
- [ ] Internet connection stable

**Time Required:** 15-20 minutes total

---

## 📋 Step-by-Step Checklist

### STEP 1: AWS Account (5 min)
- [ ] Go to aws.amazon.com
- [ ] Click "Create an AWS Account"
- [ ] Enter email and account name
- [ ] Create password
- [ ] Add contact information
- [ ] Add payment method
- [ ] Verify identity (SMS/call)
- [ ] Choose "Basic support - Free"
- [ ] Wait for confirmation email
- [ ] **STATUS: AWS Account Created ✅**

---

### STEP 2: Sign In (1 min)
- [ ] Go to console.aws.amazon.com
- [ ] Click "Sign in to the Console"
- [ ] Select "Root user"
- [ ] Enter email and password
- [ ] Click "Sign in"
- [ ] **STATUS: Signed In ✅**

---

### STEP 3: Push to GitHub (3 min)
- [ ] Create GitHub account (if needed)
- [ ] Create new repository: `pharma-intelligence-api`
- [ ] Make it Public
- [ ] Run these commands:
  ```bash
  cd /Users/administrator/.openclaw/workspace
  git init
  git add .
  git commit -m "Initial commit"
  git remote add origin https://github.com/YOUR_USERNAME/pharma-intelligence-api.git
  git push -u origin main
  ```
- [ ] Verify code is on GitHub
- [ ] **STATUS: Code on GitHub ✅**

---

### STEP 4: Create App Runner Service (5 min)

#### Connect Source:
- [ ] Search "App Runner" in AWS Console
- [ ] Click "Create service"
- [ ] Choose "Source code repository"
- [ ] Click "Add new" for GitHub
- [ ] Authorize AWS Connector
- [ ] Select your repository
- [ ] Select `main` branch
- [ ] Set deployment to "Automatic"
- [ ] Click "Next"

#### Configure Build:
- [ ] Build method: "Dockerfile"
- [ ] Dockerfile path: `api/Dockerfile`
- [ ] Dockerfile context: `.`
- [ ] Click "Next"

#### Service Settings:
- [ ] Service name: `pharma-intelligence-api`
- [ ] vCPU: `1`
- [ ] Memory: `2 GB`
- [ ] Add environment variable:
  - Key: `ENV`
  - Value: `production`
- [ ] Port: `8000`
- [ ] Health check path: `/health`
- [ ] Health check interval: `20` seconds
- [ ] Auto scaling:
  - Max concurrency: `100`
  - Min size: `1`
  - Max size: `3`
- [ ] Click "Next"

#### Review & Deploy:
- [ ] Review all settings
- [ ] Note estimated cost: ~$12-25/month (less with free tier)
- [ ] Click "Create & Deploy"
- [ ] **STATUS: Deployment Started ✅**

---

### STEP 5: Wait & Monitor (5-10 min)
- [ ] Watch deployment status
- [ ] Wait for "Running" (green) status
- [ ] Copy API URL (looks like: `https://abc123.us-east-1.awsapprunner.com`)
- [ ] Save this URL somewhere safe
- [ ] **STATUS: API Deployed ✅**

---

### STEP 6: Test API (2 min)
- [ ] Test health endpoint:
  ```bash
  curl https://YOUR-URL.awsapprunner.com/health
  ```
- [ ] Open API docs in browser:
  ```
  https://YOUR-URL.awsapprunner.com/docs
  ```
- [ ] Test country endpoint:
  ```bash
  curl https://YOUR-URL.awsapprunner.com/api/country/au
  ```
- [ ] **STATUS: API Working ✅**

---

### STEP 7: Connect Frontend (2 min)
- [ ] Create `frontend/src/config.ts`:
  ```typescript
  export const API_BASE_URL = import.meta.env.PROD
    ? 'https://YOUR-URL.awsapprunner.com'
    : 'http://localhost:8000'
  ```
- [ ] Update API calls to use `API_BASE_URL`
- [ ] Add CORS in App Runner:
  - Go to Configuration tab
  - Add environment variable:
    - Key: `CORS_ORIGINS`
    - Value: `http://localhost:3000,https://your-frontend.com`
- [ ] Wait 2-3 minutes for redeployment
- [ ] Test frontend connection
- [ ] **STATUS: Frontend Connected ✅**

---

## 🎉 Deployment Complete!

### You Should Now Have:
- ✅ AWS account created
- ✅ App Runner service running
- ✅ API accessible via HTTPS
- ✅ Automatic scaling enabled
- ✅ Frontend connected
- ✅ Health monitoring active

### Your URLs:
- **API Base:** https://YOUR-URL.awsapprunner.com
- **Health:** https://YOUR-URL.awsapprunner.com/health
- **Docs:** https://YOUR-URL.awsapprunner.com/docs
- **Countries:** https://YOUR-URL.awsapprunner.com/api/countries

---

## 🚨 Troubleshooting

### If Deployment Fails:
1. Check GitHub repo is Public
2. Verify Dockerfile path: `api/Dockerfile`
3. Check logs in App Runner console
4. Verify all files pushed to GitHub

### If Service is Unhealthy:
1. Check health endpoint path: `/health`
2. Verify port: `8000`
3. Check logs for startup errors
4. Verify environment variables

### If Frontend Can't Connect:
1. Add CORS_ORIGINS environment variable
2. Include your frontend URL
3. Wait for automatic redeployment
4. Check browser console for errors

---

## 💰 Cost Monitoring

### Set Up Billing Alert:
1. Go to AWS Billing console
2. Click "Billing preferences"
3. Check "Receive Billing Alerts"
4. Create CloudWatch alarm for $10 threshold

### Check Current Costs:
1. AWS Billing Dashboard
2. View by service
3. App Runner costs shown separately

### Expected Costs:
- **Free Tier (First 12 months):** Likely $0-5/month
- **After Free Tier:** $5-15/month for low traffic
- **High Traffic:** Scales with usage

---

## 📊 Next Steps

### Immediate:
- [ ] Test all API endpoints
- [ ] Deploy frontend to production
- [ ] Set up custom domain (optional)
- [ ] Configure monitoring alerts

### This Week:
- [ ] Monitor costs daily
- [ ] Test frontend-backend integration
- [ ] Set up CloudWatch alarms
- [ ] Document API URL for team

### This Month:
- [ ] Review AWS bill
- [ ] Optimize instance size if needed
- [ ] Add authentication (if required)
- [ ] Set up backup strategy

---

## 📞 Support Resources

### Documentation:
- **This Guide:** DEPLOY_TO_AWS_APPRUNNER.md
- **AWS App Runner Docs:** https://docs.aws.amazon.com/apprunner/
- **AWS Support:** https://console.aws.amazon.com/support/

### Quick Links:
- **AWS Console:** https://console.aws.amazon.com
- **App Runner:** https://console.aws.amazon.com/apprunner
- **Billing:** https://console.aws.amazon.com/billing
- **CloudWatch:** https://console.aws.amazon.com/cloudwatch

### Common Commands:
```bash
# Test health
curl https://YOUR-URL.awsapprunner.com/health

# Test API
curl https://YOUR-URL.awsapprunner.com/api/countries

# View logs (AWS Console)
# App Runner → Service → Logs tab

# Check metrics (AWS Console)
# App Runner → Service → Metrics tab
```

---

## ✅ Success Criteria

You're successful when all these are true:
- ✅ Health endpoint returns `{"status": "healthy"}`
- ✅ API docs page loads at `/docs`
- ✅ Can query `/api/countries` successfully
- ✅ Can query `/api/country/au` successfully
- ✅ Frontend can make API calls without CORS errors
- ✅ Response time < 500ms
- ✅ Service status shows "Running" (green)
- ✅ No errors in CloudWatch logs

---

## 🎯 Performance Benchmarks

### Expected Performance:
- **Cold Start:** < 3 seconds (first request after idle)
- **Warm Response:** < 100ms
- **Health Check:** < 50ms
- **Data Queries:** < 300ms
- **Large Queries:** < 1 second

### If Performance is Slow:
1. Check instance size (upgrade to 2 vCPU if needed)
2. Enable response caching
3. Optimize database queries
4. Add CloudFront CDN

---

## 🔒 Security Checklist

- [ ] HTTPS enabled (automatic with App Runner)
- [ ] CORS configured for specific domains
- [ ] Environment variables for secrets
- [ ] Health checks enabled
- [ ] Logs enabled
- [ ] Billing alerts set up
- [ ] MFA enabled on AWS account (recommended)

---

**Last Updated:** 2026-02-04
**Deployment Method:** AWS App Runner
**Estimated Time:** 15 minutes
**Difficulty:** ⭐ Beginner-friendly
**Cost:** ~$5-15/month (likely FREE first year)
