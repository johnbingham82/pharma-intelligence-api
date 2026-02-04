# AWS Amplify Deployment Guide

## Quick Setup (5 minutes)

### 1. Push to GitHub
```bash
cd /Users/administrator/.openclaw/workspace
git add frontend/amplify.yml AMPLIFY_DEPLOYMENT.md
git commit -m "Add AWS Amplify configuration"
git push origin main
```

### 2. Deploy via AWS Amplify Console

1. **Open AWS Amplify Console:**
   - Go to: https://console.aws.amazon.com/amplify/
   - Click **"New app"** → **"Host web app"**

2. **Connect GitHub:**
   - Select **GitHub** as the repository provider
   - Click **"Connect GitHub"**
   - Authorize AWS Amplify to access your repositories
   - Select repository: `pharma-intelligence-api`
   - Select branch: `main`

3. **Configure Build Settings:**
   - Amplify will auto-detect the `amplify.yml` in the `frontend/` folder
   - App root directory: `frontend`
   - Build command: `npm run build` (auto-detected)
   - Output directory: `dist` (auto-detected)
   - Click **"Next"**

4. **Environment Variables:**
   Add this environment variable:
   - Key: `VITE_API_URL`
   - Value: `https://pharma-intelligence-api-ee752ce1773a.herokuapp.com`
   
   Click **"Next"**

5. **Review & Deploy:**
   - Review settings
   - Click **"Save and deploy"**

### 3. Wait for Deployment (3-5 minutes)
Amplify will:
- Provision build environment
- Clone your repo
- Run `npm ci` and `npm run build`
- Deploy to CloudFront CDN

### 4. Get Your URL
Once deployed, you'll get a URL like:
```
https://main.d1a2b3c4d5e6f7.amplifyapp.com
```

---

## Environment Variables

The frontend uses these environment variables:

- **`VITE_API_URL`** (required): Backend API URL
  - Production: `https://pharma-intelligence-api-ee752ce1773a.herokuapp.com`
  - Local dev: `http://localhost:8000`

Set in Amplify Console: **App Settings** → **Environment variables**

---

## Automatic Deployments

Once connected:
- Every push to `main` branch → auto-deploys to production
- Pull requests → auto-generates preview URLs
- Rollback available in Amplify Console

---

## Custom Domain (Optional)

1. Go to **Domain management** in Amplify Console
2. Click **"Add domain"**
3. Enter your domain (e.g., `app.yourcompany.com`)
4. Follow DNS verification steps
5. Amplify auto-provisions SSL certificate

---

## Cost

AWS Amplify pricing:
- **Build minutes:** $0.01/minute (free tier: 1000 minutes/month)
- **Hosting:** $0.15/GB served + $0.023/GB stored
- **Estimate:** $1-10/month for typical usage

Free tier covers most development work.

---

## Troubleshooting

### Build fails with "Module not found"
- Check `package.json` has all dependencies
- Verify `amplify.yml` has correct `baseDirectory: dist`

### API calls fail after deployment
- Verify `VITE_API_URL` environment variable is set
- Check CORS settings in backend API allow your Amplify domain

### Custom headers not working
- Edit `customHeaders` section in `amplify.yml`
- Redeploy from Amplify Console

---

## Monitoring

View logs and metrics:
- **Build logs:** Amplify Console → Select your app → Build history
- **Access logs:** CloudWatch Logs (if enabled)
- **Performance:** CloudWatch metrics for CloudFront

---

## Support

- [AWS Amplify Documentation](https://docs.aws.amazon.com/amplify/)
- [Amplify GitHub](https://github.com/aws-amplify/amplify-hosting)
