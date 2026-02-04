# Pharma Intelligence API - Deployment Guide

## 🚀 Quick Start (Docker - Recommended)

### Prerequisites
- **Docker** installed ([Get Docker](https://docs.docker.com/get-docker/))
- **Docker Compose** installed (usually comes with Docker Desktop)

### Deploy in 2 Commands

```bash
# 1. Build the Docker image
./deploy.sh build

# 2. Start the API
./deploy.sh start
```

The API will be available at:
- **API:** http://localhost:8000
- **Docs:** http://localhost:8000/docs
- **Health:** http://localhost:8000/health

---

## 📋 Deployment Commands

### Basic Commands

```bash
# Build Docker images (first time only)
./deploy.sh build

# Start services
./deploy.sh start

# Stop services
./deploy.sh stop

# Restart services
./deploy.sh restart

# View logs
./deploy.sh logs

# Check status
./deploy.sh status

# Clean up everything
./deploy.sh clean
```

### Manual Docker Commands

```bash
# Build
docker-compose build

# Start (detached)
docker-compose up -d

# View logs
docker-compose logs -f api

# Stop
docker-compose down

# Rebuild and restart
docker-compose up -d --build
```

---

## 🔧 Configuration

### Environment Variables

Create `.env` file in the project root:

```env
# API Configuration
ENV=production
PORT=8000
CORS_ORIGINS=http://localhost:3000,https://yourfrontend.com

# Database (optional - future)
DATABASE_URL=postgresql://user:password@localhost:5432/pharma_intel

# Redis (optional - future)
REDIS_URL=redis://localhost:6379/0

# Security (optional - future)
SECRET_KEY=your-secret-key-here
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### CORS Configuration

By default, the API allows requests from:
- `http://localhost:3000` (Vite dev server)
- `http://localhost:5173` (Alternative Vite port)

To add more origins, update `docker-compose.yml`:

```yaml
environment:
  - CORS_ORIGINS=http://localhost:3000,https://yourapp.com
```

---

## 🌐 Production Deployment

### Option 1: AWS ECS (Elastic Container Service)

**1. Build and push to ECR:**

```bash
# Login to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin YOUR_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com

# Build for ARM64 (Graviton) or AMD64
docker build -t pharma-api --platform linux/amd64 api/

# Tag
docker tag pharma-api:latest YOUR_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com/pharma-api:latest

# Push
docker push YOUR_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com/pharma-api:latest
```

**2. Create ECS Task Definition:**

```json
{
  "family": "pharma-api",
  "containerDefinitions": [
    {
      "name": "api",
      "image": "YOUR_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com/pharma-api:latest",
      "portMappings": [
        {
          "containerPort": 8000,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {
          "name": "ENV",
          "value": "production"
        }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/pharma-api",
          "awslogs-region": "us-east-1",
          "awslogs-stream-prefix": "ecs"
        }
      }
    }
  ],
  "requiresCompatibilities": ["FARGATE"],
  "networkMode": "awsvpc",
  "cpu": "256",
  "memory": "512"
}
```

**3. Create ECS Service with ALB**

---

### Option 2: AWS Lambda (Serverless)

**Using Mangum adapter:**

```bash
# Add to requirements.txt
mangum==0.17.0

# Update main.py
from mangum import Mangum
handler = Mangum(app)

# Deploy with AWS SAM or Serverless Framework
```

---

### Option 3: Google Cloud Run

```bash
# Build and push
gcloud builds submit --tag gcr.io/YOUR_PROJECT/pharma-api api/

# Deploy
gcloud run deploy pharma-api \
  --image gcr.io/YOUR_PROJECT/pharma-api \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --port 8000
```

---

### Option 4: Heroku

**Using Heroku CLI:**

```bash
# Login
heroku login

# Create app
heroku create pharma-intelligence-api

# Add buildpack
heroku buildpacks:set heroku/python

# Deploy
git subtree push --prefix api heroku main

# Or use container
heroku container:push web -a pharma-intelligence-api
heroku container:release web -a pharma-intelligence-api
```

**Procfile:**
```
web: uvicorn main:app --host=0.0.0.0 --port=${PORT:-8000}
```

---

### Option 5: Digital Ocean App Platform

**app.yaml:**

```yaml
name: pharma-api
services:
  - name: api
    github:
      repo: your-username/pharma-intelligence
      branch: main
      deploy_on_push: true
    source_dir: /api
    dockerfile_path: api/Dockerfile
    http_port: 8000
    instance_count: 1
    instance_size_slug: basic-xxs
    routes:
      - path: /
    health_check:
      http_path: /health
    envs:
      - key: ENV
        value: production
```

---

### Option 6: Fly.io

**fly.toml:**

```toml
app = "pharma-api"
primary_region = "sjc"

[build]
  dockerfile = "api/Dockerfile"

[http_service]
  internal_port = 8000
  force_https = true
  auto_stop_machines = true
  auto_start_machines = true
  min_machines_running = 0

[[services.ports]]
  port = 80
  handlers = ["http"]
  force_https = true

[[services.ports]]
  port = 443
  handlers = ["tls", "http"]

[services.concurrency]
  type = "connections"
  hard_limit = 25
  soft_limit = 20

[[services.tcp_checks]]
  interval = "15s"
  timeout = "2s"
  grace_period = "5s"
  restart_limit = 0
```

**Deploy:**
```bash
fly launch
fly deploy
```

---

## 🔒 Security Considerations

### Production Checklist:

- [ ] **Environment Variables** - Use secrets management (AWS Secrets Manager, etc.)
- [ ] **HTTPS** - Enable SSL/TLS (Let's Encrypt, AWS Certificate Manager)
- [ ] **CORS** - Restrict to production domains only
- [ ] **Rate Limiting** - Add rate limiting middleware
- [ ] **Authentication** - Implement JWT or API keys
- [ ] **Input Validation** - Already handled by Pydantic
- [ ] **Logging** - Configure production logging
- [ ] **Monitoring** - Add APM (DataDog, New Relic, CloudWatch)
- [ ] **Database** - Use managed database service
- [ ] **Backups** - Set up automated backups
- [ ] **CDN** - Use CloudFront or Cloudflare for static assets

---

## 📊 Monitoring & Logging

### Health Check Endpoint

```bash
curl http://localhost:8000/health
```

**Response:**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "timestamp": "2026-02-04T13:30:00Z",
  "data_sources": {
    "UK": "available",
    "US": "available",
    "AU": "available",
    // ...
  }
}
```

### CloudWatch Logs (AWS)

```python
# Add to main.py
import logging
from pythonjsonlogger import jsonlogger

logger = logging.getLogger()
logHandler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter()
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)
logger.setLevel(logging.INFO)
```

### Prometheus Metrics

```bash
# Add to requirements.txt
prometheus-fastapi-instrumentator==6.1.0

# Add to main.py
from prometheus_fastapi_instrumentator import Instrumentator

Instrumentator().instrument(app).expose(app)
```

---

## 🐛 Troubleshooting

### Container won't start

```bash
# Check logs
docker-compose logs api

# Check container status
docker ps -a

# Rebuild without cache
docker-compose build --no-cache
```

### Port already in use

```bash
# Find process using port 8000
lsof -i :8000

# Kill the process
kill -9 <PID>

# Or change port in docker-compose.yml
ports:
  - "8001:8000"
```

### Can't connect to API from frontend

1. **Check CORS settings** in docker-compose.yml
2. **Check firewall** rules
3. **Check container network**:
   ```bash
   docker network inspect pharma-network
   ```

### Data source errors

1. **Check data files** are copied:
   ```bash
   docker exec -it pharma-api ls -la
   ```

2. **Check PBS data**:
   ```bash
   docker exec -it pharma-api ls -la pbs_data/
   ```

3. **Mount volumes** in docker-compose.yml if needed

---

## 🔄 CI/CD Pipeline

### GitHub Actions

**.github/workflows/deploy.yml:**

```yaml
name: Deploy API

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.12'
      
      - name: Install dependencies
        run: |
          cd api
          pip install -r requirements.txt
      
      - name: Run tests
        run: |
          cd api
          pytest

  deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v2
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: us-east-1
      
      - name: Login to Amazon ECR
        uses: aws-actions/amazon-ecr-login@v1
      
      - name: Build and push
        run: |
          docker build -t pharma-api api/
          docker tag pharma-api:latest $ECR_REGISTRY/pharma-api:latest
          docker push $ECR_REGISTRY/pharma-api:latest
      
      - name: Deploy to ECS
        run: |
          aws ecs update-service --cluster pharma-cluster --service pharma-api --force-new-deployment
```

---

## 📈 Performance Optimization

### Enable Caching

```python
# Add Redis caching
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis

@app.on_event("startup")
async def startup():
    redis = aioredis.from_url("redis://localhost")
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
```

### Enable Compression

```python
from fastapi.middleware.gzip import GZipMiddleware
app.add_middleware(GZipMiddleware, minimum_size=1000)
```

### Horizontal Scaling

```yaml
# docker-compose.yml
services:
  api:
    deploy:
      replicas: 3
  
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
```

---

## ✅ Deployment Checklist

- [ ] Docker images built successfully
- [ ] API starts without errors
- [ ] Health check endpoint responding
- [ ] All data sources loading correctly
- [ ] CORS configured for frontend domain
- [ ] Environment variables set
- [ ] Logs working correctly
- [ ] Frontend can connect to API
- [ ] All endpoints tested
- [ ] Performance acceptable
- [ ] Security headers configured
- [ ] SSL/TLS enabled
- [ ] Monitoring set up
- [ ] Backups configured

---

## 📞 Support

- **Documentation:** This file + API docs at `/docs`
- **Issues:** GitHub Issues
- **Logs:** `./deploy.sh logs`
- **Status:** `./deploy.sh status`

---

**Last Updated:** 2026-02-04
**API Version:** 1.0.0
**Docker:** Required
