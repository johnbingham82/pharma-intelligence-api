# AWS App Runner - One-Page Cheat Sheet

## 🚀 Quick Commands

### Push to GitHub:
```bash
cd /Users/administrator/.openclaw/workspace
git init && git add . && git commit -m "Deploy API"
git remote add origin https://github.com/YOUR_USERNAME/pharma-intelligence-api.git
git push -u origin main
```

### Test API:
```bash
# Replace YOUR-URL with your actual URL
curl https://YOUR-URL.awsapprunner.com/health
curl https://YOUR-URL.awsapprunner.com/api/countries
open https://YOUR-URL.awsapprunner.com/docs
```

---

## 📋 App Runner Configuration

### Source Settings:
- **Repository:** `your-username/pharma-intelligence-api`
- **Branch:** `main`
- **Deployment:** `Automatic`

### Build Settings:
- **Method:** `Dockerfile`
- **Dockerfile path:** `api/Dockerfile`
- **Context:** `.` (root)

### Service Settings:
- **Name:** `pharma-intelligence-api`
- **vCPU:** `1`
- **Memory:** `2 GB`
- **Port:** `8000`

### Environment Variables:
```
ENV = production
CORS_ORIGINS = http://localhost:3000,https://your-frontend.com
```

### Health Check:
- **Path:** `/health`
- **Interval:** `20` seconds
- **Timeout:** `5` seconds

### Auto Scaling:
- **Max concurrency:** `100`
- **Min size:** `1`
- **Max size:** `3`

---

## 🔗 Important Links

| Link | URL |
|------|-----|
| **AWS Console** | https://console.aws.amazon.com |
| **App Runner** | https://console.aws.amazon.com/apprunner |
| **Billing** | https://console.aws.amazon.com/billing |
| **Support** | https://console.aws.amazon.com/support |

---

## ✅ Deployment Checklist

- [ ] AWS account created
- [ ] Code pushed to GitHub (Public repo)
- [ ] App Runner service created
- [ ] Status shows "Running" (green)
- [ ] API URL copied
- [ ] Health endpoint works
- [ ] API docs accessible
- [ ] Frontend connected
- [ ] CORS configured
- [ ] Billing alert set

---

## 🐛 Quick Fixes

**Build fails?**
→ Check Dockerfile path: `api/Dockerfile`

**Unhealthy?**
→ Verify health path: `/health` and port: `8000`

**CORS errors?**
→ Add `CORS_ORIGINS` environment variable

**Slow?**
→ Upgrade to 2 vCPU in configuration

---

## 💰 Cost Estimate

- **Free Tier:** $0 (first 12 months)
- **After:** $5-15/month
- **High traffic:** $15-30/month

---

## 📊 Expected Performance

- **Cold Start:** < 3 seconds
- **Warm Response:** < 100ms
- **Health Check:** < 50ms
- **API Calls:** < 300ms

---

## 🎯 Success Criteria

✅ Health returns: `{"status": "healthy"}`
✅ Docs load at: `/docs`
✅ Countries work: `/api/countries`
✅ No CORS errors
✅ Status: "Running" (green)

---

**Your API URL:** `https://_____________.us-east-1.awsapprunner.com`
**Deployment Time:** ~20 minutes
**Support Doc:** DEPLOY_TO_AWS_APPRUNNER.md
