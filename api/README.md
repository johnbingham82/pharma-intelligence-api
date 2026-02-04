# Pharma Intelligence API

**FastAPI Backend for Drug Analysis Platform**

REST API that wraps the generalized pharma intelligence engine, providing instant prescribing pattern analysis for any drug in any supported country.

---

## 🚀 Quick Start

### 1. Install Dependencies

```bash
cd /Users/administrator/.openclaw/workspace
pip install -r api/requirements.txt
```

### 2. Start the Server

```bash
# Development mode (auto-reload)
python api/main.py

# OR with uvicorn directly
uvicorn api.main:app --reload --port 8000
```

### 3. Open the Docs

**Swagger UI:** http://localhost:8000/docs  
**ReDoc:** http://localhost:8000/redoc

### 4. Test the API

```bash
python api/test_api.py
```

---

## 📡 API Endpoints

### General

**`GET /`** - API information  
**`GET /health`** - Health check with data source status

### Reference Data

**`GET /countries`** - List supported countries and data sources

### Drug Search

**`POST /drugs/search`** - Search for drugs by name
```json
{
  "query": "metformin",
  "country": "UK",
  "limit": 10
}
```

**`GET /drugs/lookup?name=metformin&country=UK`** - Quick drug code lookup

### Analysis (Core)

**`POST /analyze`** - Comprehensive drug analysis
```json
{
  "company": "Novartis",
  "drug_name": "Inclisiran",
  "country": "UK",
  "region": null,
  "top_n": 50,
  "scorer": "market_share"
}
```

**Response:**
```json
{
  "drug": {
    "name": "Inclisiran",
    "generic_name": "inclisiran",
    "therapeutic_area": "Cardiovascular",
    "company": "Novartis"
  },
  "market_summary": {
    "total_prescribers": 4520,
    "total_prescriptions": 45230,
    "total_cost": 12500000.0
  },
  "top_opportunities": [
    {
      "rank": 1,
      "prescriber_id": "Y12345",
      "prescriber_name": "High Street Medical",
      "current_volume": 450,
      "opportunity_score": 1523.5,
      "recommendations": [
        "⭐ KEY ACCOUNT: Maintain strong relationship"
      ]
    }
  ],
  "segments": {
    "by_volume": {
      "High Prescribers": 120,
      "Medium Prescribers": 580
    }
  }
}
```

---

## 🧪 Testing

### Run Full Test Suite

```bash
python api/test_api.py
```

### Manual Testing with cURL

```bash
# Health check
curl http://localhost:8000/health

# List countries
curl http://localhost:8000/countries

# Search drugs
curl -X POST http://localhost:8000/drugs/search \
  -H "Content-Type: application/json" \
  -d '{"query":"metformin","country":"UK","limit":5}'

# Analyze drug
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "company": "Generic",
    "drug_name": "metformin",
    "country": "UK",
    "top_n": 10
  }'
```

### Testing with Python requests

```python
import requests

# Analyze a drug
response = requests.post(
    "http://localhost:8000/analyze",
    json={
        "company": "Novartis",
        "drug_name": "inclisiran",
        "country": "UK",
        "top_n": 20
    }
)

data = response.json()
print(f"Total prescribers: {data['market_summary']['total_prescribers']}")
print(f"Top opportunity: {data['top_opportunities'][0]['prescriber_name']}")
```

---

## 🏗️ Architecture

```
api/
├── __init__.py          # Package init
├── main.py              # FastAPI application
├── routes.py            # API endpoints
├── models.py            # Pydantic request/response models
├── requirements.txt     # Dependencies
├── test_api.py          # Test suite
└── README.md            # This file
```

### Key Components

**main.py** - FastAPI app with middleware, CORS, error handlers  
**routes.py** - REST endpoints using intelligence engine  
**models.py** - Type-safe request/response validation (Pydantic)  
**test_api.py** - Automated testing of all endpoints

---

## 📊 Response Models

### AnalysisResponse
- `drug` - Drug metadata
- `market_summary` - Total prescribers, volume, cost
- `top_opportunities` - Ranked list of prescribers
- `segments` - Volume & opportunity-based segmentation

### OpportunityResponse
- `rank` - Position in top opportunities
- `prescriber_id` - Unique identifier
- `prescriber_name` - Practice/prescriber name
- `current_volume` - Current prescription count
- `opportunity_score` - Calculated opportunity score
- `recommendations` - List of actionable insights

### ErrorResponse
- `error` - Error message
- `detail` - Additional context
- `timestamp` - When error occurred

---

## 🔒 Authentication (Coming Soon)

Currently open for testing. Production will add:

**JWT Bearer Tokens**
```bash
curl -H "Authorization: Bearer <token>" \
  http://localhost:8000/analyze
```

**API Keys**
```bash
curl -H "X-API-Key: <key>" \
  http://localhost:8000/analyze
```

**Rate Limiting**
- Free tier: 10 requests/hour
- Paid tier: Unlimited

---

## 🌍 Supported Countries

### Currently Available
- ✅ **UK** - NHS OpenPrescribing API

### Coming Soon
- 🚧 **US** - Medicare Part D data
- 🚧 **Germany** - National health data
- 🚧 **France** - National health data
- 🚧 **Spain** - National health data

---

## ⚙️ Configuration

### Environment Variables

```bash
# API Configuration
export API_HOST=0.0.0.0
export API_PORT=8000
export API_ENV=development  # development, staging, production

# Data Sources
export UK_API_KEY=<optional>  # For rate-limited APIs

# Authentication (future)
export JWT_SECRET=<secret>
export JWT_ALGORITHM=HS256
export ACCESS_TOKEN_EXPIRE_MINUTES=30

# Database (future)
export DATABASE_URL=postgresql://user:pass@localhost/pharma_intel

# Redis Cache (future)
export REDIS_URL=redis://localhost:6379/0
```

### Production Deployment

```bash
# Install production server
pip install gunicorn

# Run with Gunicorn (production)
gunicorn api.main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000 \
  --timeout 120
```

---

## 🚀 Performance

### Benchmarks (UK, Single Drug)

| Metric | Value |
|--------|-------|
| **Data Fetch** | 5-10 seconds |
| **Analysis** | <1 second |
| **Total Response** | 6-11 seconds |
| **Memory** | ~100 MB per worker |

### Optimization Tips

1. **Enable caching** - Redis for drug lookups
2. **Async workers** - Use multiple Uvicorn workers
3. **Database** - Store drug catalog locally
4. **CDN** - Cache static country/drug lists
5. **Background jobs** - Queue long analyses with Celery

---

## 🐛 Debugging

### Enable Debug Mode

```python
# In api/main.py
app = FastAPI(debug=True)
```

### Check Logs

```bash
# Server logs (if using systemd)
journalctl -u pharma-api -f

# Development logs
python api/main.py 2>&1 | tee api.log
```

### Common Issues

**"Cannot connect to API"**
- Check server is running: `curl http://localhost:8000/health`
- Check port is not blocked: `lsof -i :8000`

**"Drug not found"**
- Verify drug name spelling
- Try drug search first: `POST /drugs/search`
- Check country is supported: `GET /countries`

**"Analysis timeout"**
- Increase uvicorn timeout: `--timeout-keep-alive 120`
- Check data source API is responding
- Try smaller `top_n` value

---

## 📈 Roadmap

### Phase 1: Core API ✅ (Current)
- [x] REST endpoints
- [x] UK data source
- [x] Error handling
- [x] API documentation
- [x] Test suite

### Phase 2: Production Features (Next 2 weeks)
- [ ] JWT authentication
- [ ] Rate limiting
- [ ] Response caching (Redis)
- [ ] Background job queue (Celery)
- [ ] Database for user management

### Phase 3: Scale (Month 2)
- [ ] US data source (Medicare)
- [ ] EU data sources (3+ countries)
- [ ] Async analysis endpoints
- [ ] WebSocket for real-time updates
- [ ] API usage analytics

### Phase 4: Advanced Features (Month 3+)
- [ ] Competitive analysis endpoints
- [ ] Time series / trend analysis
- [ ] Geographic clustering
- [ ] Custom scoring algorithms (user-defined)
- [ ] Batch analysis endpoints

---

## 🤝 Integration Examples

### Frontend (React)

```javascript
// Analyze a drug
const response = await fetch('http://localhost:8000/analyze', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    company: 'Novartis',
    drug_name: 'Inclisiran',
    country: 'UK',
    top_n: 50
  })
});

const data = await response.json();
console.log(`Found ${data.market_summary.total_prescribers} prescribers`);
```

### Python Client

```python
import requests

class PharmaIntelClient:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
    
    def analyze_drug(self, company, drug_name, country, top_n=50):
        response = requests.post(
            f"{self.base_url}/analyze",
            json={
                "company": company,
                "drug_name": drug_name,
                "country": country,
                "top_n": top_n
            }
        )
        response.raise_for_status()
        return response.json()

# Usage
client = PharmaIntelClient()
result = client.analyze_drug("Novartis", "inclisiran", "UK")
```

---

## 📝 API Versioning

Future versions will be namespaced:

- **v1** (current): `/analyze`, `/drugs/search`
- **v2** (future): `/v2/analyze`, `/v2/drugs/search`

Old versions supported for 6 months after new release.

---

## 📞 Support

**Issues:** Report bugs via GitHub issues  
**Documentation:** http://localhost:8000/docs  
**Status:** http://localhost:8000/health

---

**Built with OpenClaw** 🦾  
*From concept to API in 90 minutes*
