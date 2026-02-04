# Pharma Intelligence Platform - Quick Start Guide

## 🚀 Deploy API (Choose One Method)

### Method 1: Docker (Recommended) ⭐

```bash
# Install Docker Desktop first: https://docs.docker.com/get-docker/

# Build
./deploy.sh build

# Start
./deploy.sh start

# Check
./deploy.sh status

# API ready at: http://localhost:8000
```

---

### Method 2: Python 3.12 (Local)

```bash
# Install Python 3.12 with pyenv
brew install pyenv
pyenv install 3.12.0
cd api && pyenv local 3.12.0
cd ..

# Deploy
./deploy_local.sh

# API ready at: http://localhost:8000
```

---

### Method 3: Cloud Platform

**Heroku (Easiest):**
```bash
heroku create pharma-api
git subtree push --prefix api heroku main
```

**AWS ECS, Google Cloud Run, etc.**
See `DEPLOYMENT_GUIDE.md` for full instructions

---

## 🖥️ Start Frontend

```bash
cd frontend
npm install
npm run dev

# Frontend ready at: http://localhost:3000
```

---

## ✅ Test Integration

```bash
# 1. Check API health
curl http://localhost:8000/health

# 2. Test country endpoint
curl http://localhost:8000/api/country/au

# 3. Open frontend
open http://localhost:3000

# 4. Navigate to Dashboard
# Click "View Global Dashboard"

# 5. Test search
# Navigate to /search
```

---

## 📊 Access Points

| Service | URL | Description |
|---------|-----|-------------|
| **Frontend** | http://localhost:3000 | Main application |
| **API** | http://localhost:8000 | REST API |
| **API Docs** | http://localhost:8000/docs | Interactive docs |
| **Health** | http://localhost:8000/health | Health check |

---

## 🎯 Main Features

### Dashboard
- Navigate to: `/dashboard`
- 7 chart types
- Animated statistics
- Export CSV/JSON

### Search
- Navigate to: `/search`
- 10 filter types
- Save presets
- Sort & export

### Country Details
- Navigate to: `/country/au`
- Heat maps
- Regional data
- Time series

### Price Comparison
- Navigate to: `/compare`
- 8-country comparison
- Key insights
- Export data

---

## 🐛 Common Issues

### API Won't Start (Python 3.14)
**Problem:** Pydantic compatibility
**Solution:** Use Docker or Python 3.12

### Port Already in Use
```bash
lsof -i :8000
kill -9 <PID>
```

### CORS Errors
Add frontend URL to `docker-compose.yml`:
```yaml
environment:
  - CORS_ORIGINS=http://localhost:3000
```

---

## 📚 Full Documentation

- **API_DEPLOYMENT_COMPLETE.md** - Deployment summary
- **DEPLOYMENT_GUIDE.md** - Comprehensive guide
- **PLATFORM_COMPLETE_STATUS.md** - Platform overview

---

## 🎉 Quick Demo

```bash
# 1. Start API (choose method above)

# 2. Start frontend
cd frontend && npm run dev

# 3. Open browser
open http://localhost:3000

# 4. Explore features
- Click "View Global Dashboard"
- Try "Advanced Search"
- Browse country cards
- View "Australia" for real PBS data
```

---

**Need Help?** Check `DEPLOYMENT_GUIDE.md` or create an issue.

**Status:** ✅ Ready to deploy!
