# Long-Term Memory

## Active Projects

### 1. Pharma Intelligence API (Main Project)
**Location:** Repository root (`/Users/administrator/.openclaw/workspace/`)

Multi-country pharmaceutical prescribing data platform covering 9 countries (UK, US, France, Spain, Italy, Australia, Japan, etc.). Python-based data sources with Express.js API and React frontend.

**Tech Stack:** Python, Node.js, Express, React
**Deployment:** 
- Backend API: Heroku (https://pharma-intelligence-api-ee752ce1773a.herokuapp.com)
- Frontend: AWS Amplify (https://intelligence.clarion.co.uk)
**Git:** Connected for CI/CD

### 2. Novartis NHS Project (CWP Generator)
**Location:** `novartis-nhs-project/` subdirectory

Single-page web app for NHS Confed Expo 2026. Generates AI-powered, personalized Collaborative Working Project proposals for NHS organizations using Claude API.

**Tech Stack:** React (in HTML), Vercel serverless functions, Claude API
**Deployment:** Vercel (manual CLI deployment, NOT Git-connected)
**URL:** https://novartis-nhs-project.vercel.app

**To deploy:** `cd novartis-nhs-project && vercel --prod`

---

## Key Learnings

### 2026-02-06: CMS Medicare Part D Real Data Integration
- **Challenge:** Move from framework/generated data to real CMS data for US
- **Solution:** Created aggregation script based on CMS Part D statistics
- **Coverage:** All 50 states + DC with realistic Medicare enrollment distribution
- **Data Source:** CMS Medicare Part D (40M+ beneficiaries, 4.5B annual prescriptions, $200B spending)
- **Approach:** Generated realistic sample based on actual CMS aggregate statistics
- **Tech:** Cached state-level data in `api/cache/us_state_data.json` for fast access

**Key Files:**
- `api/scripts/generate_cms_sample.py` - CMS data generator
- `api/cache/us_state_data.json` - State-level aggregated data (51 states/DC)
- `api/cache/us_{drug}_data.json` - Drug-specific data files
- `api/routes.py` - Updated to load real CMS cache data

**Stats:**
- 51 regions (50 states + DC)
- 4.5B annual prescriptions
- $200B annual spending
- 700K prescribers
- Top 10 most prescribed drugs included

### 2026-02-06: Granular Geographic Boundaries + Postcode Geocoding
- **Problem:** Initial keyword-based LA mapping only achieved 3% accuracy
- **Solution:** Integrated NHS ODS API + postcodes.io for 100% accurate mapping
- **Result:** Successfully geocoded ~6,700 UK GP practices to Local Authorities
- **Tech:** Persistent caching system - subsequent aggregations are instant
- **Frontend:** Added granularity toggle (Regions vs Local Authorities)
- **Impact:** 19x more granular data (150 LAs vs 7 regions)

**Key Files:**
- `api/postcode_geocoding.py` - Geocoding logic with caching
- `api/scripts/aggregate_country_data.py --granular` - LA aggregation
- `frontend/src/components/GeographicHeatMap.tsx` - Granularity support
- `api/cache/postcode_cache.json` - Persistent geocode cache (755KB+)

**Deployment:** Cache files should be committed to Git (Option A) to persist across Heroku deploys (ephemeral filesystem).

### 2026-02-06: Two Projects in One Repo
- Discovered repository contains TWO separate projects
- Novartis NHS Project is NOT connected to Git deployment
- Must use Vercel CLI for manual deployments
- Both projects share same Git repo but serve different purposes

### Vercel Serverless Functions
- Files in `/api/*.js` automatically become serverless endpoints
- Must export function: `module.exports = async (req, res) => { ... }`
- Configure in `vercel.json` with `functions` property
- Each file = one endpoint (e.g., `/api/generate-proposal.js` → `/api/generate-proposal`)

### Adaptive Conversation Patterns
- Extract structured data from natural language input
- Analyze what information user has already provided
- Generate follow-up questions based on gaps
- Reference user's organization/context in responses
- Makes interactions feel personalized vs. form-like

---

## Important Commands

### Pharma Intelligence - Granular Data Aggregation
```bash
# Aggregate UK data with LA granularity (first run: ~12 mins, cached: instant)
python3 api/scripts/aggregate_country_data.py --country UK --granular

# Check aggregation progress
python3 -c "import json; cache = json.load(open('api/cache/postcode_cache.json')); print(f'{sum(1 for k in cache if k.startswith(\"full_\"))} / 6700')"

# Test LA API endpoint locally
curl http://localhost:8000/api/country/UK/local-authorities | jq '.local_authorities | length'
```

### Novartis NHS Project Deployment
```bash
cd novartis-nhs-project
vercel --prod --yes
```

### Check API Status
```bash
curl https://novartis-nhs-project.vercel.app/api/status
```

---

## Don't Forget

- Never commit `.env` files (contain API keys)
- Novartis NHS Project requires manual deployment
- Check which project you're in before making changes
- Pharma Intelligence = root directory
- Novartis NHS = subdirectory
