# Pharma Intelligence API - Quick Start

**Get the API running in 2 minutes**

---

## 🚀 Option 1: Automated Setup (Recommended)

```bash
cd /Users/administrator/.openclaw/workspace

# 1. Run setup (creates venv, installs dependencies)
./api/setup.sh

# 2. Start the server
./api/start.sh
```

**That's it!** API will be running at http://localhost:8000

---

## 🛠️ Option 2: Manual Setup

```bash
cd /Users/administrator/.openclaw/workspace

# 1. Create virtual environment
python3 -m venv venv

# 2. Activate it
source venv/bin/activate

# 3. Install dependencies
pip install -r api/requirements.txt

# 4. Start the server
python api/main.py
```

---

## 📖 Open the Docs

Once running, open your browser:

**Swagger UI:** http://localhost:8000/docs  
**ReDoc:** http://localhost:8000/redoc

---

## 🧪 Test It Works

**Option A: Browser**

Open http://localhost:8000/health in your browser. You should see:
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "data_sources": {
    "UK": "available"
  }
}
```

**Option B: Command Line**

```bash
# In a new terminal (keep server running)
curl http://localhost:8000/health
```

**Option C: Run Test Suite**

```bash
# Activate venv first
source venv/bin/activate

# Run tests
python api/test_api.py
```

---

## 🎯 Try Your First Analysis

### Using the Swagger UI (Easiest)

1. Open http://localhost:8000/docs
2. Find **POST /analyze**
3. Click "Try it out"
4. Use this example:
   ```json
   {
     "company": "Generic",
     "drug_name": "metformin",
     "country": "UK",
     "top_n": 10
   }
   ```
5. Click "Execute"

### Using cURL

```bash
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "company": "Generic",
    "drug_name": "metformin",
    "country": "UK",
    "top_n": 10
  }'
```

### Using Python

```python
import requests

response = requests.post(
    "http://localhost:8000/analyze",
    json={
        "company": "Generic",
        "drug_name": "metformin",
        "country": "UK",
        "top_n": 10
    }
)

data = response.json()
print(f"Total prescribers: {data['market_summary']['total_prescribers']:,}")
print(f"Top opportunity: {data['top_opportunities'][0]['prescriber_name']}")
```

---

## 📁 Project Structure

```
workspace/
├── pharma_intelligence_engine.py   # Core analysis engine
├── data_sources_uk.py              # UK data adapter
│
├── api/                            # FastAPI backend
│   ├── main.py                     # FastAPI app
│   ├── routes.py                   # API endpoints
│   ├── models.py                   # Request/response models
│   ├── requirements.txt            # Dependencies
│   ├── README.md                   # Full API docs
│   ├── test_api.py                 # Test suite
│   ├── setup.sh                    # Setup script
│   └── start.sh                    # Start script
│
├── venv/                           # Virtual environment (created by setup)
└── API_QUICKSTART.md               # This file
```

---

## 🔥 Available Endpoints

### Core Analysis
- **POST /analyze** - Run comprehensive drug analysis
- **POST /drugs/search** - Search for drug codes
- **GET /drugs/lookup** - Quick drug code lookup

### Reference
- **GET /countries** - List supported countries
- **GET /health** - API health check
- **GET /** - API info

See full docs at http://localhost:8000/docs

---

## 🐛 Troubleshooting

### "Module not found: fastapi"
Run the setup script: `./api/setup.sh`

### "Address already in use"
Port 8000 is taken. Either:
- Stop other service: `lsof -ti:8000 | xargs kill`
- Or change port in `api/main.py`: `port=8001`

### "Cannot connect to API"
Make sure server is running: `./api/start.sh`

### Tests fail with "Connection refused"
Server needs to be running in a separate terminal

---

## ⏭️ Next Steps

1. ✅ **API Running** - You're here
2. **Try Different Drugs** - Test with inclisiran, atorvastatin, etc.
3. **Read Full Docs** - See `api/README.md` for all features
4. **Build Frontend** - Use API to power web UI
5. **Add Countries** - Create US/EU data sources

---

## 📚 Documentation

- **Quick Start** - This file
- **Full API Docs** - `api/README.md`
- **Core Engine** - `PHARMA_ENGINE_README.md`
- **V1 vs V2** - `V1_VS_V2_COMPARISON.md`
- **Interactive Docs** - http://localhost:8000/docs

---

## 💡 Example Workflow

```bash
# 1. Setup (one time)
./api/setup.sh

# 2. Start server (terminal 1)
./api/start.sh

# 3. Test API (terminal 2)
source venv/bin/activate
python api/test_api.py

# 4. Try manual requests
curl http://localhost:8000/health
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"company":"Novartis","drug_name":"inclisiran","country":"UK","top_n":20}'
```

---

## 🎯 What You Can Do Now

**Analyze any drug in the UK:**
- Metformin (diabetes)
- Atorvastatin (cholesterol)
- Salbutamol (asthma)
- Pembrolizumab (cancer)
- Inclisiran (cardiovascular)
- ...and 1000s more

**Get instant insights:**
- Top prescriber opportunities
- Market segmentation
- Actionable recommendations
- Total market size & spend

---

**Time to first analysis:** < 2 minutes 🚀  
**From concept to working API:** 90 minutes 🦾
